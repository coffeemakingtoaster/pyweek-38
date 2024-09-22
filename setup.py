from setuptools import setup

setup(
    name='Dish Deception',
    options={
        'build_apps': {
            'gui_apps': {
                'Dish Deception': 'main.py',
            },

            # Set up output logging, important for GUI apps!
            'log_filename': './logs/output.log',
            'log_append': False,

            # Specify which files are included with the distribution
            'include_patterns': [
                'assets/**/*',
                'user_config.json',
                'map.json',
                '*.png'
            ],

            # Include the OpenGL renderer and OpenAL audio plug-in
            'plugins': [
                'pandagl',
                'p3openal_audio',
                'p3ffmpeg',
                'p3assimp'
            ],
            'icons': {
                    'Dish Deception': ['assets/icon.png']
                },
            'prefer_discrete_gpu': True
        }
    }
)
