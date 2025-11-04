# No Qt platform plugin could be initialized

```shell
uv run preprocessor gui
```

If you get this error:

```
qt.qpa.plugin: From 6.5.0, xcb-cursor0 or libxcb-cursor0 is needed to load the Qt xcb platform plugin.
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: vnc, xcb, wayland-brcm, wayland-egl, wayland, offscreen, eglfs, minimalegl, minimal, vkkhrdisplay, linuxfb.
```

This solved it on Ubuntu:

```shell
sudo apt install -y libxcb-cursor-dev
```

# Cannot create platform OpenGL context, neither GLX nor EGL are enabled

```shell
uv run preprocessor gui
```

If you get this error:

```
QXcbIntegration: Cannot create platform OpenGL context, neither GLX nor EGL are enabled
QRhiGles2: Failed to create temporary context
QXcbIntegration: Cannot create platform offscreen surface, neither GLX nor EGL are enabled
QXcbIntegration: Cannot create platform OpenGL context, neither GLX nor EGL are enabled
QRhiGles2: Failed to create context
Failed to create RHI (backend 2)
Failed to initialize graphics backend for OpenGL.
```

Ensure you don't have an existing Conda environment activated that may interfere with the system OpenGL libraries. Deactivate any Conda environment and try again.

```shell
conda deactivate
uv run preprocessor gui
```

If it's the `base` environment, which activates by default, you can disable auto-activation:

```shell
conda config --set auto_activate false
```
