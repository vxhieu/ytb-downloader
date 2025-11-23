#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Video Snapshot Tool
Tool để trích xuất snapshot từ video theo khoảng thời gian định sẵn
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import os
import json
import threading
from pathlib import Path
from datetime import timedelta


class VideoSnapshotTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Snapshot Tool")
        self.root.geometry("800x750")
        self.root.resizable(True, True)
        
        # Modern color scheme
        self.colors = {
            'bg': '#f5f5f5',
            'fg': '#333333',
            'primary': '#4a90e2',
            'primary_hover': '#357abd',
            'success': '#5cb85c',
            'danger': '#d9534f',
            'warning': '#f0ad4e',
            'info': '#5bc0de',
            'light': '#ffffff',
            'dark': '#2c3e50',
            'border': '#dee2e6'
        }
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
        # Variables
        self.video_path = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.interval_option = tk.IntVar(value=3)  # Default: 3 seconds
        self.custom_interval = tk.StringVar(value="")
        self.is_processing = False
        self.should_stop = False
        
        # Video info
        self.video_info = {
            'duration': 0,
            'fps': 0,
            'width': 0,
            'height': 0,
            'total_frames': 0
        }
        
        # Store entry widgets for styling
        self.video_entry = None
        self.output_entry = None
        
        # Config file path
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        
        # Load config
        self.config = self.load_config()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        # Create scrollable main frame
        main_canvas = tk.Canvas(self.root, bg=self.colors['bg'], highlightthickness=0)
        main_scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, 
                                     command=main_canvas.yview,
                                     bg=self.colors['bg'],
                                     troughcolor=self.colors['bg'],
                                     activebackground=self.colors['primary'])
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        # Main frame with modern styling
        main_frame = tk.Frame(main_canvas, bg=self.colors['bg'], padx=20, pady=20)
        main_canvas_window = main_canvas.create_window((0, 0), window=main_frame, anchor=tk.NW)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Pack canvas and scrollbar
        main_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Update scroll region when frame size changes
        def on_frame_configure(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            # Update canvas window width
            canvas_width = event.width
            main_canvas.itemconfig(main_canvas_window, width=canvas_width)
        
        main_frame.bind('<Configure>', on_frame_configure)
        main_canvas.bind('<Configure>', lambda e: main_canvas.itemconfig(main_canvas_window, width=e.width))
        
        # Bind mouse wheel to main canvas (hỗ trợ cả Windows và Linux)
        def on_main_mousewheel(event):
            # Windows và macOS
            if hasattr(event, 'delta') and event.delta:
                main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            # Linux
            elif hasattr(event, 'num'):
                if event.num == 4:
                    main_canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    main_canvas.yview_scroll(1, "units")
        
        # Bind cho Windows/Mac
        main_canvas.bind("<MouseWheel>", on_main_mousewheel)
        # Bind cho Linux
        main_canvas.bind("<Button-4>", on_main_mousewheel)
        main_canvas.bind("<Button-5>", on_main_mousewheel)
        
        # Đảm bảo canvas có thể nhận focus
        main_canvas.focus_set()
        
        # Bind mouse wheel cho tất cả widgets con trong main_frame
        def bind_mousewheel_to_widgets(widget):
            try:
                widget.bind("<MouseWheel>", on_main_mousewheel)
                widget.bind("<Button-4>", on_main_mousewheel)
                widget.bind("<Button-5>", on_main_mousewheel)
                for child in widget.winfo_children():
                    bind_mousewheel_to_widgets(child)
            except:
                pass  # Một số widget không thể bind
        
        # Bind cho main_frame và các widget con
        bind_mousewheel_to_widgets(main_frame)
        
        # Bind cho root window để scroll khi hover bất kỳ đâu
        def on_root_mousewheel(event):
            # Chỉ scroll nếu không phải đang hover preview canvas
            x, y = self.root.winfo_pointerx(), self.root.winfo_pointery()
            widget = self.root.winfo_containing(x, y)
            
            # Nếu không phải preview canvas, scroll main canvas
            if widget != self.preview_canvas and not str(widget).startswith(str(self.preview_canvas)):
                on_main_mousewheel(event)
        
        self.root.bind_all("<MouseWheel>", on_root_mousewheel)
        self.root.bind_all("<Button-4>", on_root_mousewheel)
        self.root.bind_all("<Button-5>", on_root_mousewheel)
        
        # Store reference for later use
        self.main_frame = main_frame
        self.main_canvas = main_canvas
        
        row = 0
        
        # Title with modern styling
        title_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        title_frame.grid(row=row, column=0, columnspan=3, pady=(0, 30), sticky=(tk.W, tk.E))
        title_label = tk.Label(title_frame, text="🎬 Video Snapshot Tool", 
                               font=("Segoe UI", 24, "bold"),
                               bg=self.colors['bg'], fg=self.colors['dark'])
        title_label.pack()
        subtitle_label = tk.Label(title_frame, text="Trích xuất snapshot từ video theo khoảng thời gian",
                                 font=("Segoe UI", 10),
                                 bg=self.colors['bg'], fg='#666666')
        subtitle_label.pack(pady=(5, 0))
        row += 1
        
        # Video selection with improved styling
        video_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        video_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        video_frame.columnconfigure(1, weight=1)
        
        video_label = tk.Label(video_frame, text="📁 File Video:", 
                              font=("Segoe UI", 10, "bold"),
                              bg=self.colors['bg'], fg=self.colors['dark'],
                              anchor='w')
        video_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Entry with placeholder-like hint
        hint_frame = tk.Frame(video_frame, bg=self.colors['light'], relief=tk.SOLID, bd=1)
        hint_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        hint_frame.columnconfigure(0, weight=1)
        
        self.video_entry = tk.Entry(hint_frame, textvariable=self.video_path, 
                                    font=("Segoe UI", 10),
                                    relief=tk.FLAT, bd=0, bg=self.colors['light'],
                                    fg=self.colors['fg'], insertbackground=self.colors['primary'])
        self.video_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=8)
        self.video_entry.bind('<KeyRelease>', lambda e: self.on_video_path_change())
        self.video_entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(self.video_entry, "Nhập đường dẫn file video hoặc click 'Chọn Video'"))
        self.video_entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(self.video_entry, "Nhập đường dẫn file video hoặc click 'Chọn Video'"))
        
        # Add placeholder text
        self.add_placeholder(self.video_entry, "Nhập đường dẫn file video hoặc click 'Chọn Video'")
        
        # Modern button styling
        select_video_btn = tk.Button(video_frame, text="📂 Chọn Video", 
                                     command=self.select_video,
                                     font=("Segoe UI", 10, "bold"),
                                     bg=self.colors['primary'], fg='white',
                                     activebackground=self.colors['primary_hover'],
                                     activeforeground='white',
                                     relief=tk.FLAT, bd=0,
                                     padx=20, pady=8,
                                     cursor='hand2')
        select_video_btn.grid(row=1, column=2, padx=(0, 0))
        row += 1
        
        # Interval selection with modern styling
        interval_frame = tk.LabelFrame(main_frame, text=" ⏱️  Khoảng thời gian snapshot", 
                                      font=("Segoe UI", 11, "bold"),
                                      bg=self.colors['light'], fg=self.colors['dark'],
                                      relief=tk.FLAT, bd=1, padx=15, pady=15)
        interval_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        interval_frame.columnconfigure(0, weight=1)
        row += 1
        
        # Radio buttons with modern styling
        intervals = [
            (3, "3 giây", "⭐ Khuyến nghị"),
            (6, "6 giây", ""),
            (9, "9 giây", ""),
            (12, "12 giây", "")
        ]
        
        for idx, (value, text, extra) in enumerate(intervals):
            rb_frame = tk.Frame(interval_frame, bg=self.colors['light'])
            rb_frame.grid(row=idx, column=0, sticky=tk.W, pady=3)
            
            rb = tk.Radiobutton(rb_frame, text=f"{text} {extra}", 
                               variable=self.interval_option, value=value,
                               command=self.on_interval_change,
                               font=("Segoe UI", 10),
                               bg=self.colors['light'], fg=self.colors['dark'],
                               activebackground=self.colors['light'],
                               activeforeground=self.colors['primary'],
                               selectcolor=self.colors['light'],
                               cursor='hand2')
            rb.pack(side=tk.LEFT)
        
        # Custom interval
        custom_frame = tk.Frame(interval_frame, bg=self.colors['light'])
        custom_frame.grid(row=4, column=0, sticky=tk.W, pady=(8, 0))
        
        custom_rb = tk.Radiobutton(custom_frame, text="Tùy chỉnh:", 
                                  variable=self.interval_option, value=0,
                                  command=self.on_interval_change,
                                  font=("Segoe UI", 10),
                                  bg=self.colors['light'], fg=self.colors['dark'],
                                  activebackground=self.colors['light'],
                                  activeforeground=self.colors['primary'],
                                  selectcolor=self.colors['light'],
                                  cursor='hand2')
        custom_rb.pack(side=tk.LEFT)
        
        custom_entry_frame = tk.Frame(custom_frame, bg=self.colors['light'], 
                                      relief=tk.SOLID, bd=1)
        custom_entry_frame.pack(side=tk.LEFT, padx=(10, 5))
        
        custom_entry = tk.Entry(custom_entry_frame, textvariable=self.custom_interval, 
                               width=8, font=("Segoe UI", 10),
                               relief=tk.FLAT, bd=0, bg=self.colors['light'],
                               fg=self.colors['fg'], insertbackground=self.colors['primary'])
        custom_entry.pack(padx=5, pady=3)
        custom_entry.bind('<KeyRelease>', lambda e: self.on_interval_change())
        
        tk.Label(custom_frame, text="giây", 
                font=("Segoe UI", 10),
                bg=self.colors['light'], fg=self.colors['fg']).pack(side=tk.LEFT)
        
        # Output folder selection with improved styling
        output_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        output_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        output_frame.columnconfigure(1, weight=1)
        
        output_label = tk.Label(output_frame, text="📂 Thư mục lưu:", 
                               font=("Segoe UI", 10, "bold"),
                               bg=self.colors['bg'], fg=self.colors['dark'],
                               anchor='w')
        output_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Entry with placeholder-like hint
        hint_frame_out = tk.Frame(output_frame, bg=self.colors['light'], relief=tk.SOLID, bd=1)
        hint_frame_out.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        hint_frame_out.columnconfigure(0, weight=1)
        
        self.output_entry = tk.Entry(hint_frame_out, textvariable=self.output_folder, 
                                     font=("Segoe UI", 10),
                                     relief=tk.FLAT, bd=0, bg=self.colors['light'],
                                     fg=self.colors['fg'], insertbackground=self.colors['primary'])
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=8)
        self.output_entry.bind('<KeyRelease>', lambda e: self.on_output_path_change())
        self.output_entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(self.output_entry, "Nhập đường dẫn thư mục hoặc click 'Chọn thư mục'"))
        self.output_entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(self.output_entry, "Nhập đường dẫn thư mục hoặc click 'Chọn thư mục'"))
        
        # Add placeholder text
        self.add_placeholder(self.output_entry, "Nhập đường dẫn thư mục hoặc click 'Chọn thư mục'")
        
        # Modern button styling
        select_folder_btn = tk.Button(output_frame, text="📁 Chọn thư mục", 
                                      command=self.select_output_folder,
                                      font=("Segoe UI", 10, "bold"),
                                      bg=self.colors['primary'], fg='white',
                                      activebackground=self.colors['primary_hover'],
                                      activeforeground='white',
                                      relief=tk.FLAT, bd=0,
                                      padx=20, pady=8,
                                      cursor='hand2')
        select_folder_btn.grid(row=1, column=2, padx=(0, 0))
        row += 1
        
        # Video info frame with modern styling
        info_frame = tk.LabelFrame(main_frame, text=" ℹ️  Thông tin video", 
                                   font=("Segoe UI", 11, "bold"),
                                   bg=self.colors['light'], fg=self.colors['dark'],
                                   relief=tk.FLAT, bd=1, padx=15, pady=15)
        info_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        info_frame.columnconfigure(0, weight=1)
        row += 1
        
        info_inner = tk.Frame(info_frame, bg=self.colors['light'])
        info_inner.pack(fill=tk.BOTH, expand=True)
        
        self.info_text = tk.Text(info_inner, height=6, width=60, state="disabled", 
                                wrap=tk.WORD, font=("Segoe UI", 10),
                                bg=self.colors['light'], fg=self.colors['dark'],
                                relief=tk.FLAT, bd=0, padx=5, pady=5)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons with modern styling
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.grid(row=row, column=0, columnspan=3, pady=15)
        row += 1
        
        self.start_button = tk.Button(button_frame, text="▶️  Bắt đầu", 
                                      command=self.start_extraction, state="disabled",
                                      font=("Segoe UI", 11, "bold"),
                                      bg=self.colors['success'], fg='white',
                                      activebackground='#4cae4c',
                                      activeforeground='white',
                                      relief=tk.FLAT, bd=0,
                                      padx=25, pady=12,
                                      cursor='hand2')
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="⏹️  Dừng", 
                                     command=self.stop_extraction, state="disabled",
                                     font=("Segoe UI", 11, "bold"),
                                     bg=self.colors['danger'], fg='white',
                                     activebackground='#c9302c',
                                     activeforeground='white',
                                     relief=tk.FLAT, bd=0,
                                     padx=25, pady=12,
                                     cursor='hand2')
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="🗑️  Xóa", 
                             command=self.clear_all,
                             font=("Segoe UI", 11, "bold"),
                             bg=self.colors['warning'], fg='white',
                             activebackground='#ec971f',
                             activeforeground='white',
                             relief=tk.FLAT, bd=0,
                             padx=25, pady=12,
                             cursor='hand2')
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        open_folder_btn = tk.Button(button_frame, text="📂 Mở thư mục", 
                                   command=self.open_output_folder,
                                   font=("Segoe UI", 11, "bold"),
                                   bg=self.colors['info'], fg='white',
                                   activebackground='#46b8da',
                                   activeforeground='white',
                                   relief=tk.FLAT, bd=0,
                                   padx=25, pady=12,
                                   cursor='hand2')
        open_folder_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress frame with modern styling
        progress_frame = tk.LabelFrame(main_frame, text=" 📊 Tiến trình", 
                                       font=("Segoe UI", 11, "bold"),
                                       bg=self.colors['light'], fg=self.colors['dark'],
                                       relief=tk.FLAT, bd=1, padx=15, pady=15)
        progress_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        progress_frame.columnconfigure(0, weight=1)
        row += 1
        
        # Custom progress bar frame
        progress_bar_frame = tk.Frame(progress_frame, bg=self.colors['light'], 
                                     relief=tk.SOLID, bd=1, height=25)
        progress_bar_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        progress_bar_frame.columnconfigure(0, weight=1)
        progress_bar_frame.grid_propagate(False)
        
        self.progress_var = tk.DoubleVar()
        self.progress_canvas = tk.Canvas(progress_bar_frame, height=23, 
                                        bg=self.colors['light'], 
                                        highlightthickness=0)
        self.progress_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=2, pady=1)
        progress_bar_frame.columnconfigure(0, weight=1)
        
        # Bind canvas resize to update progress bar
        def on_canvas_resize(event):
            if hasattr(self, 'progress_var'):
                progress = self.progress_var.get()
                width = event.width
                if width > 1:
                    fill_width = int(width * progress / 100)
                    self.progress_canvas.delete("progress")
                    self.progress_canvas.create_rectangle(0, 0, fill_width, 23, 
                                                         fill=self.colors['success'],
                                                         outline="", tags="progress")
        self.progress_canvas.bind('<Configure>', on_canvas_resize)
        
        self.progress_label = tk.Label(progress_frame, text="Chưa bắt đầu",
                                       font=("Segoe UI", 10),
                                       bg=self.colors['light'], fg=self.colors['fg'])
        self.progress_label.grid(row=1, column=0, pady=5)
        
        # Preview frame with modern styling and scrollable canvas
        preview_frame = tk.LabelFrame(main_frame, text=" 🖼️  Preview", 
                                      font=("Segoe UI", 11, "bold"),
                                      bg=self.colors['light'], fg=self.colors['dark'],
                                      relief=tk.FLAT, bd=1, padx=15, pady=15)
        preview_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=15)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        row += 1
        
        # Create scrollable canvas for preview
        preview_container = tk.Frame(preview_frame, bg=self.colors['light'])
        preview_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas with scrollbars
        self.preview_canvas = tk.Canvas(preview_container, bg=self.colors['light'],
                                        highlightthickness=0, relief=tk.FLAT)
        
        # Vertical scrollbar
        v_scrollbar = tk.Scrollbar(preview_container, orient=tk.VERTICAL, 
                                   command=self.preview_canvas.yview,
                                   bg=self.colors['light'],
                                   troughcolor=self.colors['bg'],
                                   activebackground=self.colors['primary'])
        self.preview_canvas.configure(yscrollcommand=v_scrollbar.set)
        
        # Horizontal scrollbar
        h_scrollbar = tk.Scrollbar(preview_container, orient=tk.HORIZONTAL,
                                   command=self.preview_canvas.xview,
                                   bg=self.colors['light'],
                                   troughcolor=self.colors['bg'],
                                   activebackground=self.colors['primary'])
        self.preview_canvas.configure(xscrollcommand=h_scrollbar.set)
        
        # Frame inside canvas for the image
        self.preview_image_frame = tk.Frame(self.preview_canvas, bg=self.colors['light'])
        self.preview_canvas_window = self.preview_canvas.create_window((0, 0), 
                                                                       window=self.preview_image_frame,
                                                                       anchor=tk.NW)
        
        # Pack scrollbars and canvas
        self.preview_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        preview_container.columnconfigure(0, weight=1)
        preview_container.rowconfigure(0, weight=1)
        
        # Bind canvas resize to update scroll region
        def on_canvas_configure(event):
            # Update scroll region
            self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all"))
            # Update canvas window width
            canvas_width = event.width
            self.preview_canvas.itemconfig(self.preview_canvas_window, width=canvas_width)
        
        self.preview_canvas.bind('<Configure>', on_canvas_configure)
        
        # Bind mouse wheel to preview canvas (hỗ trợ cả Windows và Linux)
        def on_preview_mousewheel(event):
            # Windows và macOS
            if hasattr(event, 'delta') and event.delta:
                self.preview_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            # Linux
            elif hasattr(event, 'num'):
                if event.num == 4:
                    self.preview_canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.preview_canvas.yview_scroll(1, "units")
            return "break"  # Prevent event propagation
        
        # Bind cho Windows/Mac
        self.preview_canvas.bind("<MouseWheel>", on_preview_mousewheel)
        # Bind cho Linux
        self.preview_canvas.bind("<Button-4>", on_preview_mousewheel)
        self.preview_canvas.bind("<Button-5>", on_preview_mousewheel)
        
        # Đảm bảo preview canvas có thể nhận focus
        self.preview_canvas.focus_set()
        
        # Bind cho preview_image_frame và các widget con
        def bind_preview_mousewheel(widget):
            try:
                widget.bind("<MouseWheel>", on_preview_mousewheel)
                widget.bind("<Button-4>", on_preview_mousewheel)
                widget.bind("<Button-5>", on_preview_mousewheel)
                for child in widget.winfo_children():
                    bind_preview_mousewheel(child)
            except:
                pass  # Một số widget không thể bind
        
        bind_preview_mousewheel(self.preview_image_frame)
        
        # Preview label inside the frame
        self.preview_label = tk.Label(self.preview_image_frame, text="Chưa có preview", 
                                      anchor=tk.CENTER,
                                      font=("Segoe UI", 10),
                                      bg=self.colors['light'], fg='#999999')
        self.preview_label.pack()
        
        # Configure row weights
        main_frame.rowconfigure(row, weight=1)
        
        # Load đường dẫn mặc định từ config
        self.load_default_paths()
    
    def load_default_paths(self):
        """Load đường dẫn mặc định từ config vào các entry"""
        # Load thư mục output mặc định
        default_output = self.config.get("default_output_folder", "")
        if default_output and os.path.exists(default_output):
            self.output_folder.set(default_output)
            if self.output_entry:
                self.output_entry.config(fg=self.colors['fg'])
        elif self.config.get("last_output_folder", ""):
            last_output = self.config.get("last_output_folder", "")
            if last_output and os.path.exists(last_output):
                self.output_folder.set(last_output)
                if self.output_entry:
                    self.output_entry.config(fg=self.colors['fg'])
        
        # Load file video cuối cùng (nếu còn tồn tại)
        last_video = self.config.get("last_video_path", "")
        if last_video and os.path.exists(last_video):
            self.video_path.set(last_video)
            if self.video_entry:
                self.video_entry.config(fg=self.colors['fg'])
            # Load thông tin video
            self.root.after(100, self.load_video_info)
        
        # Cập nhật trạng thái nút
        self.update_start_button_state()
    
    def load_config(self):
        """Load cấu hình từ file JSON"""
        default_config = {
            "default_video_folder": "",
            "default_output_folder": "",
            "last_video_path": "",
            "last_output_folder": ""
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge với default để đảm bảo có tất cả keys
                    for key in default_config:
                        if key not in config:
                            config[key] = default_config[key]
                    return config
            else:
                # Tạo file config mặc định
                self.save_config(default_config)
                return default_config
        except Exception as e:
            print(f"Lỗi khi đọc config: {e}")
            return default_config
    
    def save_config(self, config=None):
        """Lưu cấu hình vào file JSON"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Lỗi khi lưu config: {e}")
    
    def add_placeholder(self, entry, placeholder_text):
        """Thêm placeholder text vào entry"""
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg='#999999')
    
    def on_entry_focus_in(self, entry, placeholder_text):
        """Xử lý khi entry được focus"""
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg=self.colors['fg'])
    
    def on_entry_focus_out(self, entry, placeholder_text):
        """Xử lý khi entry mất focus"""
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg='#999999')
    
    def select_video(self):
        """Chọn file video"""
        # Lấy thư mục mặc định từ config
        initial_dir = self.config.get("default_video_folder", "")
        if not initial_dir or not os.path.exists(initial_dir):
            # Nếu không có hoặc không tồn tại, dùng thư mục của file video cuối cùng
            last_path = self.config.get("last_video_path", "")
            if last_path and os.path.exists(last_path):
                initial_dir = os.path.dirname(last_path)
            else:
                initial_dir = os.path.expanduser("~")
        
        file_path = filedialog.askopenfilename(
            title="Chọn video file",
            initialdir=initial_dir,
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv"),
                ("MP4 files", "*.mp4"),
                ("AVI files", "*.avi"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.video_path.set(file_path)
            # Remove placeholder styling if present
            if self.video_entry:
                self.video_entry.config(fg=self.colors['fg'])
            
            # Lưu đường dẫn vào config
            self.config["last_video_path"] = file_path
            self.config["default_video_folder"] = os.path.dirname(file_path)
            self.save_config()
            
            self.load_video_info()
            self.update_start_button_state()
    
    def on_video_path_change(self):
        """Callback khi đường dẫn video thay đổi"""
        path = self.video_path.get()
        # Remove placeholder text if user is typing
        if self.video_entry and path and path != "Nhập đường dẫn file video hoặc click 'Chọn Video'":
            self.video_entry.config(fg=self.colors['fg'])
        
        if path and os.path.exists(path):
            self.load_video_info()
        self.update_start_button_state()
    
    def on_output_path_change(self):
        """Callback khi đường dẫn output thay đổi"""
        path = self.output_folder.get()
        # Remove placeholder text if user is typing
        if self.output_entry and path and path != "Nhập đường dẫn thư mục hoặc click 'Chọn thư mục'":
            self.output_entry.config(fg=self.colors['fg'])
        self.update_start_button_state()
    
    def select_output_folder(self):
        """Chọn thư mục output"""
        # Lấy thư mục mặc định từ config
        initial_dir = self.config.get("default_output_folder", "")
        if not initial_dir or not os.path.exists(initial_dir):
            # Nếu không có hoặc không tồn tại, dùng thư mục output cuối cùng
            last_folder = self.config.get("last_output_folder", "")
            if last_folder and os.path.exists(last_folder):
                initial_dir = last_folder
            else:
                initial_dir = os.path.expanduser("~")
        
        folder_path = filedialog.askdirectory(
            title="Chọn thư mục lưu snapshot",
            initialdir=initial_dir
        )
        
        if folder_path:
            self.output_folder.set(folder_path)
            # Remove placeholder styling if present
            if self.output_entry:
                self.output_entry.config(fg=self.colors['fg'])
            
            # Lưu đường dẫn vào config
            self.config["last_output_folder"] = folder_path
            self.config["default_output_folder"] = folder_path
            self.save_config()
            
            self.update_start_button_state()
    
    def load_video_info(self):
        """Load thông tin video"""
        video_path = self.video_path.get()
        if not video_path or not os.path.exists(video_path):
            return
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                messagebox.showerror("Lỗi", "Không thể đọc file video!")
                return
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            duration = total_frames / fps if fps > 0 else 0
            
            self.video_info = {
                'duration': duration,
                'fps': fps,
                'width': width,
                'height': height,
                'total_frames': total_frames
            }
            
            cap.release()
            
            # Update info display
            self.update_video_info_display()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi đọc video: {str(e)}")
    
    def update_video_info_display(self):
        """Cập nhật hiển thị thông tin video"""
        info = self.video_info
        interval = self.get_interval()
        
        duration_str = str(timedelta(seconds=int(info['duration'])))
        expected_snapshots = int(info['duration'] / interval) if interval > 0 else 0
        
        info_text = f"Độ dài: {duration_str}\n"
        info_text += f"FPS: {info['fps']:.2f}\n"
        info_text += f"Resolution: {info['width']}x{info['height']}\n"
        info_text += f"Tổng số frame: {info['total_frames']}\n"
        info_text += f"Khoảng thời gian: {interval} giây\n"
        info_text += f"Số snapshot dự kiến: {expected_snapshots}"
        
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info_text)
        self.info_text.config(state="disabled")
    
    def get_interval(self):
        """Lấy giá trị interval (giây)"""
        if self.interval_option.get() == 0:  # Custom
            try:
                interval = float(self.custom_interval.get())
                if interval <= 0:
                    return 3  # Default
                return interval
            except ValueError:
                return 3  # Default
        else:
            return float(self.interval_option.get())
    
    def on_interval_change(self):
        """Callback khi interval thay đổi"""
        if self.video_path.get() and os.path.exists(self.video_path.get()):
            self.update_video_info_display()
    
    def update_start_button_state(self):
        """Cập nhật trạng thái nút Start"""
        video_path_val = self.video_path.get()
        output_path_val = self.output_folder.get()
        
        # Check if paths are not placeholder text
        video_placeholder = "Nhập đường dẫn file video hoặc click 'Chọn Video'"
        output_placeholder = "Nhập đường dẫn thư mục hoặc click 'Chọn thư mục'"
        
        has_video = bool(video_path_val and 
                        video_path_val != video_placeholder and 
                        os.path.exists(video_path_val))
        has_output = bool(output_path_val and output_path_val != output_placeholder)
        
        if has_video and has_output and not self.is_processing:
            self.start_button.config(state="normal", 
                                    bg=self.colors['success'],
                                    activebackground='#4cae4c')
        else:
            self.start_button.config(state="disabled",
                                     bg='#cccccc',
                                     activebackground='#cccccc')
    
    def start_extraction(self):
        """Bắt đầu quá trình trích xuất snapshot"""
        if self.is_processing:
            return
        
        # Validate
        interval = self.get_interval()
        if interval <= 0:
            messagebox.showerror("Lỗi", "Khoảng thời gian phải lớn hơn 0!")
            return
        
        video_path_val = self.video_path.get()
        video_placeholder = "Nhập đường dẫn file video hoặc click 'Chọn Video'"
        if not video_path_val or video_path_val == video_placeholder:
            messagebox.showerror("Lỗi", "Vui lòng chọn hoặc nhập đường dẫn file video!")
            return
        
        if not os.path.exists(video_path_val):
            messagebox.showerror("Lỗi", "File video không tồn tại!")
            return
        
        output_dir = self.output_folder.get()
        output_placeholder = "Nhập đường dẫn thư mục hoặc click 'Chọn thư mục'"
        if not output_dir or output_dir == output_placeholder:
            messagebox.showerror("Lỗi", "Vui lòng chọn hoặc nhập đường dẫn thư mục lưu!")
            return
        
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tạo thư mục: {str(e)}")
                return
        
        # Check write permission
        if not os.access(output_dir, os.W_OK):
            messagebox.showerror("Lỗi", f"Không có quyền ghi vào thư mục: {output_dir}")
            return
        
        # Start processing in separate thread
        self.is_processing = True
        self.should_stop = False
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        thread = threading.Thread(target=self.extract_snapshots, daemon=True)
        thread.start()
    
    def stop_extraction(self):
        """Dừng quá trình trích xuất"""
        self.should_stop = True
        self.progress_label.config(text="Đang dừng...")
    
    def extract_snapshots(self):
        """Trích xuất snapshot từ video"""
        video_path = self.video_path.get()
        output_folder = self.output_folder.get()
        interval = self.get_interval()
        
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                self.root.after(0, lambda: messagebox.showerror("Lỗi", "Không thể đọc video!"))
                self.is_processing = False
                self.root.after(0, self.reset_buttons)
                return
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            # Calculate number of snapshots
            num_snapshots = int(duration / interval)
            frame_interval = int(fps * interval)
            
            # Ensure we have at least 1 snapshot
            if num_snapshots == 0:
                num_snapshots = 1
                frame_interval = total_frames
            
            snapshot_count = 0
            
            # Create log file
            log_file = os.path.join(output_folder, "extraction_log.txt")
            with open(log_file, 'w', encoding='utf-8') as log:
                log.write(f"Video Snapshot Extraction Log\n")
                log.write(f"{'='*50}\n")
                log.write(f"Video: {video_path}\n")
                log.write(f"Output folder: {output_folder}\n")
                log.write(f"Interval: {interval} seconds\n")
                log.write(f"FPS: {fps:.2f}\n")
                log.write(f"Duration: {duration:.2f} seconds\n")
                log.write(f"Total frames: {total_frames}\n")
                log.write(f"Expected snapshots: {num_snapshots}\n")
                log.write(f"Frame interval: {frame_interval} frames\n")
                log.write(f"{'='*50}\n\n")
                log.write(f"{'No.':<6} {'Timestamp':<12} {'Filename':<30} {'Time (MM:SS)'}\n")
                log.write(f"{'-'*70}\n")
            
            # Debug: Log thông tin chi tiết
            debug_info = []
            debug_info.append(f"Starting extraction: {num_snapshots} snapshots expected")
            debug_info.append(f"Frame interval: {frame_interval} frames")
            debug_info.append(f"FPS: {fps}, Duration: {duration}s, Total frames: {total_frames}")
            debug_info.append(f"Output folder exists: {os.path.exists(output_folder)}")
            debug_info.append(f"Output folder writable: {os.access(output_folder, os.W_OK) if os.path.exists(output_folder) else 'N/A'}")
            
            # Reset to beginning
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            for i in range(num_snapshots):
                if self.should_stop:
                    break
                
                # Calculate frame index
                frame_index = int(i * frame_interval)
                
                # Ensure frame_index doesn't exceed total_frames
                if frame_index >= total_frames:
                    frame_index = total_frames - 1
                
                # Seek to frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
                
                # Verify we're at the right frame (some codecs may not seek exactly)
                actual_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                debug_info.append(f"Seeking to frame {frame_index}, actual position: {actual_frame}")
                
                # Read frame
                ret, frame = cap.read()
                
                if not ret:
                    debug_info.append(f"Failed to read frame at index {frame_index} (actual: {actual_frame})")
                    # Try reading next few frames
                    for attempt in range(5):
                        ret, frame = cap.read()
                        if ret:
                            debug_info.append(f"Successfully read frame after {attempt+1} attempts")
                            break
                    if not ret:
                        debug_info.append(f"Failed to read frame after multiple attempts at {frame_index}")
                        continue
                
                # Check if frame is valid
                if frame is None or frame.size == 0:
                    debug_info.append(f"Invalid frame at index {frame_index} (size: {frame.size if frame is not None else 'None'})")
                    continue
                
                # Calculate timestamp
                timestamp_seconds = i * interval
                minutes = int(timestamp_seconds // 60)
                seconds = int(timestamp_seconds % 60)
                timestamp_str = f"{minutes:03d}{seconds:02d}"
                
                # Save snapshot
                filename = f"snapshot_{timestamp_str}_{snapshot_count+1:04d}.png"
                filepath = os.path.join(output_folder, filename)
                
                # Save with error checking
                success = cv2.imwrite(filepath, frame)
                if not success:
                    debug_info.append(f"Failed to save snapshot: {filepath}")
                    # Check if directory exists and is writable
                    if not os.path.exists(output_folder):
                        debug_info.append(f"Output folder does not exist: {output_folder}")
                    elif not os.access(output_folder, os.W_OK):
                        debug_info.append(f"Output folder is not writable: {output_folder}")
                    continue
                
                # Verify file was created
                if not os.path.exists(filepath):
                    debug_info.append(f"File was not created: {filepath}")
                    continue
                
                snapshot_count += 1
                debug_info.append(f"Successfully created snapshot {snapshot_count}: {filename}")
                
                # Write to log file
                time_str = f"{minutes:02d}:{seconds:02d}"
                with open(log_file, 'a', encoding='utf-8') as log:
                    log.write(f"{snapshot_count:<6} {timestamp_seconds:<12.2f} {filename:<30} {time_str}\n")
                
                # Update progress
                progress = (i + 1) / num_snapshots * 100
                self.root.after(0, lambda p=progress, c=snapshot_count, t=num_snapshots: 
                               self.update_progress(p, c, t))
                
                # Update preview (every 3 snapshots or last one)
                if snapshot_count % 3 == 0 or i == num_snapshots - 1:
                    # Create a copy of frame for thread safety
                    frame_copy = frame.copy()
                    self.root.after(0, lambda f=frame_copy: self.update_preview(f))
            
            cap.release()
            
            # Finalize log file with debug info
            with open(log_file, 'a', encoding='utf-8') as log:
                log.write(f"\n{'='*70}\n")
                log.write("Debug Information:\n")
                log.write(f"{'-'*70}\n")
                for info in debug_info:
                    log.write(f"{info}\n")
                log.write(f"\n{'='*70}\n")
                if self.should_stop:
                    log.write(f"Process stopped. Total snapshots created: {snapshot_count}\n")
                else:
                    log.write(f"Process completed. Total snapshots created: {snapshot_count}\n")
                log.write(f"{'='*70}\n")
            
            # Completion message
            if snapshot_count == 0:
                error_msg = "Không có snapshot nào được tạo!\n\n"
                error_msg += "Nguyên nhân có thể:\n"
                error_msg += "1. Không thể đọc frame từ video\n"
                error_msg += "2. Thư mục output không có quyền ghi\n"
                error_msg += "3. Video file bị lỗi hoặc format không hỗ trợ\n\n"
                error_msg += f"Xem chi tiết trong log file:\n{log_file}"
                self.root.after(0, lambda: messagebox.showerror("Lỗi", error_msg))
            elif self.should_stop:
                message = f"Đã dừng. Đã tạo {snapshot_count} snapshot.\n\nLog file đã được lưu tại:\n{log_file}"
                self.root.after(0, lambda: messagebox.showinfo("Thông báo", message))
            else:
                message = f"Hoàn thành! Đã tạo {snapshot_count} snapshot.\n\nLog file đã được lưu tại:\n{log_file}"
                self.root.after(0, lambda: messagebox.showinfo("Thông báo", message))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi khi xử lý: {str(e)}"))
        
        finally:
            self.is_processing = False
            self.root.after(0, self.reset_buttons)
    
    def update_progress(self, progress, current, total):
        """Cập nhật thanh tiến trình"""
        self.progress_var.set(progress)
        self.progress_label.config(text=f"Đã tạo: {current}/{total} snapshots ({progress:.1f}%)")
        
        # Update custom progress bar
        if hasattr(self, 'progress_canvas'):
            self.progress_canvas.delete("progress")
            width = self.progress_canvas.winfo_width()
            if width > 1:
                fill_width = int(width * progress / 100)
                self.progress_canvas.create_rectangle(0, 0, fill_width, 23, 
                                                     fill=self.colors['success'],
                                                     outline="", tags="progress")
            else:
                # Canvas not yet rendered, schedule update
                self.root.after(10, lambda: self.update_progress(progress, current, total))
    
    def update_preview(self, frame):
        """Cập nhật preview với khả năng scroll"""
        try:
            # Resize frame for preview (max 800x600 để có thể scroll xem ảnh lớn hơn)
            height, width = frame.shape[:2]
            max_width, max_height = 800, 600
            
            # Giữ nguyên kích thước nếu ảnh nhỏ hơn max, nhưng không resize quá nhỏ
            if width > max_width or height > max_height:
                scale = min(max_width / width, max_height / height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                frame = cv2.resize(frame, (new_width, new_height))
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PhotoImage
            from PIL import Image, ImageTk
            image = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(image)
            
            # Clear previous image
            if hasattr(self, 'preview_label'):
                self.preview_label.pack_forget()
                if hasattr(self.preview_label, 'image'):
                    del self.preview_label.image
            
            # Create new label with image
            self.preview_label = tk.Label(self.preview_image_frame, image=photo, 
                                         anchor=tk.NW, bg=self.colors['light'])
            self.preview_label.image = photo  # Keep a reference
            self.preview_label.pack()
            
            # Update scroll region after image is packed
            self.preview_canvas.update_idletasks()
            bbox = self.preview_canvas.bbox("all")
            if bbox:
                self.preview_canvas.configure(scrollregion=bbox)
            
        except Exception as e:
            print(f"Error updating preview: {e}")
    
    def reset_buttons(self):
        """Reset trạng thái các nút"""
        self.stop_button.config(state="disabled",
                               bg='#cccccc',
                               activebackground='#cccccc')
        self.update_start_button_state()
    
    def clear_all(self):
        """Xóa tất cả lựa chọn"""
        self.video_path.set("")
        self.output_folder.set("")
        self.interval_option.set(3)
        self.custom_interval.set("")
        self.progress_var.set(0)
        self.progress_label.config(text="Chưa bắt đầu")
        
        # Reset preview
        self.preview_label.pack_forget()
        self.preview_label = tk.Label(self.preview_image_frame, text="Chưa có preview", 
                                      anchor=tk.CENTER,
                                      font=("Segoe UI", 10),
                                      bg=self.colors['light'], fg='#999999')
        self.preview_label.pack()
        if hasattr(self.preview_label, 'image'):
            del self.preview_label.image
        self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all"))
        
        # Reset progress bar
        if hasattr(self, 'progress_canvas'):
            self.progress_canvas.delete("progress")
        
        # Reset placeholder text
        if self.video_entry:
            self.video_entry.delete(0, tk.END)
            self.add_placeholder(self.video_entry, "Nhập đường dẫn file video hoặc click 'Chọn Video'")
        if self.output_entry:
            self.output_entry.delete(0, tk.END)
            self.add_placeholder(self.output_entry, "Nhập đường dẫn thư mục hoặc click 'Chọn thư mục'")
        
        self.info_text.config(state="normal")
        self.info_text.delete(1.0, tk.END)
        self.info_text.config(state="disabled")
        
        self.video_info = {
            'duration': 0,
            'fps': 0,
            'width': 0,
            'height': 0,
            'total_frames': 0
        }
        
        self.update_start_button_state()
    
    def open_output_folder(self):
        """Mở thư mục output"""
        folder = self.output_folder.get()
        if not folder or not os.path.exists(folder):
            messagebox.showwarning("Cảnh báo", "Thư mục không tồn tại hoặc chưa được chọn!")
            return
        
        import subprocess
        import platform
        
        try:
            # Kiểm tra nếu đang chạy trong WSL
            is_wsl = False
            if platform.system() == "Linux":
                # Kiểm tra xem có phải WSL không
                try:
                    with open("/proc/version", "r") as f:
                        version_info = f.read().lower()
                        if "microsoft" in version_info or "wsl" in version_info:
                            is_wsl = True
                except:
                    pass
            
            # Nếu là WSL và đường dẫn là Windows path (/mnt/...)
            if is_wsl and folder.startswith("/mnt/"):
                # Chuyển đổi /mnt/d/... thành D:\...
                parts = folder.split("/")
                if len(parts) >= 3 and parts[1] == "mnt":
                    drive_letter = parts[2].upper()
                    windows_path = f"{drive_letter}:\\" + "\\".join(parts[3:])
                    # Sử dụng explorer.exe qua wsl
                    try:
                        subprocess.Popen(["wslview", windows_path], 
                                       stdout=subprocess.DEVNULL, 
                                       stderr=subprocess.DEVNULL)
                        return
                    except:
                        # Nếu wslview không có, thử dùng cmd.exe
                        try:
                            subprocess.Popen(["cmd.exe", "/c", "start", "", windows_path],
                                           stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL)
                            return
                        except:
                            # Fallback: thử explorer.exe trực tiếp
                            try:
                                subprocess.Popen(["explorer.exe", windows_path.replace("/", "\\")],
                                               stdout=subprocess.DEVNULL,
                                               stderr=subprocess.DEVNULL)
                                return
                            except:
                                pass
            
            # Xử lý cho Windows native
            if platform.system() == "Windows":
                try:
                    os.startfile(folder)
                    return
                except:
                    # Fallback cho Windows
                    try:
                        subprocess.Popen(["explorer.exe", folder],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)
                        return
                    except:
                        pass
            
            # Xử lý cho macOS
            elif platform.system() == "Darwin":
                try:
                    subprocess.Popen(["open", folder],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                    return
                except:
                    pass
            
            # Xử lý cho Linux (không phải WSL)
            else:
                # Thử các phương pháp mở thư mục trên Linux
                methods = [
                    ["xdg-open", folder],
                    ["nautilus", folder],
                    ["dolphin", folder],
                    ["thunar", folder],
                    ["pcmanfm", folder],
                    ["nemo", folder]
                ]
                
                for method in methods:
                    try:
                        result = subprocess.run(method, 
                                              stdout=subprocess.DEVNULL,
                                              stderr=subprocess.DEVNULL,
                                              timeout=2)
                        if result.returncode == 0:
                            return
                    except (FileNotFoundError, subprocess.TimeoutExpired):
                        continue
                
                # Nếu tất cả đều thất bại, hiển thị thông báo
                messagebox.showinfo("Thông tin", 
                                  f"Không thể mở thư mục tự động.\n\n"
                                  f"Đường dẫn: {folder}\n\n"
                                  f"Vui lòng mở thư mục thủ công.")
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở thư mục:\n{str(e)}\n\nĐường dẫn: {folder}")


def main():
    root = tk.Tk()
    app = VideoSnapshotTool(root)
    root.mainloop()


if __name__ == "__main__":
    main()

