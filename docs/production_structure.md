AI Cinematic Video Creator Engine V5

├── app.py
├── main.py
├── requirements.txt
├── README.md
│
├── .github 
│   └── workflows
│       ├── render-test.yml
│       └── render.yml
│
├── engine
│   ├── core
│   │   ├── frame_engine.py
│   │   ├── motion_engine.py
│   │   ├── segment_engine.py
│   │   ├── storage_manager.py
│   │   └── video_renderer.py
│   │
│   ├── audio_engine.py
│   ├── effects_engine.py
│   └── transition_engine.py
│
├── docs
│   ├── architecture.md
│   ├── roadmap.md
│   └── screenshots
│
├── assets
│
├── output
│
└── utils
    ├── ffmpeg.py
    ├── helpers.py
    └── image_loader.py