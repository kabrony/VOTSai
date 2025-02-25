# UI Customization Guide

TRILOGY Brain features a Matrix-inspired terminal interface that can be customized to match your visual preferences and branding needs.

## Custom Styling

### Changing the Matrix Terminal Appearance

The MatrixTerminal class in `ui/matrix_terminal.py` handles the UI styling. You can modify the `_setup_css` method to change the appearance:

```python
def _setup_css(self):
    """Set up the Matrix terminal CSS"""
    st.markdown("""
    <style>
    /* Matrix Terminal UI */
    :root {
        /* Change these variables to customize colors */
        --neon-green: #00ff41;  /* Main terminal color */
        --dark-bg: #0d0d0d;     /* Background color */
        --matrix-font: 'Courier New', monospace;  /* Font family */
    }
    
    /* Other styles... */
    </style>
    """, unsafe_allow_html=True)
```

### Custom Color Schemes

Here are some alternative color schemes you can use:

#### Cyberpunk Blue

```css
:root {
    --neon-blue: #00ffff;
    --dark-bg: #0a001a;
    --matrix-font: 'Courier New', monospace;
}

.matrix-terminal {
    background-color: var(--dark-bg);
    border: 1px solid var(--neon-blue);
    color: var(--neon-blue);
    /* Other styles... */
}
```

#### Retro Amber

```css
:root {
    --amber: #ffb000;
    --dark-bg: #100800;
    --matrix-font: 'VT323', monospace;
}

.matrix-terminal {
    background-color: var(--dark-bg);
    border: 1px solid var(--amber);
    color: var(--amber);
    /* Other styles... */
}
```

## Branding Customization

To change the branding, modify the `display_header` method in `ui/matrix_terminal.py`:

```python
def display_header(self):
    """Display the terminal header"""
    st.markdown("""
    <div class="matrix-header">
        <div class="matrix-title">YOUR CUSTOM TITLE</div>
        <div class="matrix-subtitle">Your Custom Subtitle</div>
        <div class="matrix-branding">
            <a href="https://your-website.com" target="_blank">
                Powered by Your Organization
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
```

## Custom Animations

### Adding Text Animation

You can implement custom text animations by modifying the `display` method:

```python
def display(self, text, typing_effect=True, typing_speed=30, animation_style="typing"):
    """
    Display text with custom animation
    
    Args:
        text: Text to display
        typing_effect: Whether to animate
        typing_speed: Speed of animation
        animation_style: "typing", "fade", or "matrix"
    """
    # Implementation for different animation styles...
```

### Custom Splash Screen

Add a splash screen when the application starts:

```python
def splash_screen(self):
    """Display a custom splash screen"""
    if not self.initialized:
        self.initialize()
    
    st.markdown("""
    <div class="matrix-splash">
        <div class="matrix-logo">YOUR LOGO</div>
        <div class="matrix-loading">
            <div class="matrix-progress-bar"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add CSS for the splash screen
    st.markdown("""
    <style>
    .matrix-splash {
        /* Styling for splash screen */
    }
    
    .matrix-logo {
        /* Logo styling */
    }
    
    .matrix-loading {
        /* Loading indicator styling */
    }
    
    @keyframes progress {
        0% { width: 0; }
        100% { width: 100%; }
    }
    
    .matrix-progress-bar {
        height: 2px;
        background-color: var(--neon-green);
        animation: progress 3s linear;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Simulate loading
    time.sleep(3)
```

## Layout Customization

### Changing Tab Organization

Modify the tab structure in `trilogy_app.py`:

```python
# Create tabs with custom names and order
tabs = st.tabs([
    "Your Custom Tab 1", 
    "Your Custom Tab 2", 
    "Documentation"
])
```

### Custom Metrics

Customize the dashboard metrics in `trilogy_app.py`:

```python
# In the dashboard tab
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Your Custom Metric",
        value="42",
        delta="↑ 15%",
        delta_color="normal"
    )
```

## Advanced Customization

For more advanced customization:

1. Extend the Streamlit theme by creating a `config.toml` file in the `.streamlit` directory
2. Use custom CSS for complex styling needs
3. Implement custom components with Streamlit Components 