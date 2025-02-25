import streamlit as st
import time
import random
import html

class MatrixTerminal:
    def __init__(self, initialize_now=False):
        # Don't initialize CSS right away
        self.initialized = False
        if initialize_now:
            self.initialize()
    
    def initialize(self):
        """Delayed initialization for the Matrix terminal"""
        if not self.initialized:
            self._setup_css()
            self.initialized = True
    
    def _setup_css(self):
        """Setup modern terminal CSS inspired by dev tools"""
        st.markdown("""
        <style>
        /* Modern Terminal Styling */
        .dev-terminal {
            background-color: #0d1117;
            color: #e6edf3;
            font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
            padding: 10px;
            border-radius: 6px;
            overflow: auto;
            height: 480px;
            position: relative;
            border: 1px solid #30363d;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }
        
        .dev-terminal:before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 30px;
            background: #161b22;
            border-bottom: 1px solid #30363d;
            border-radius: 6px 6px 0 0;
            display: flex;
            align-items: center;
            padding: 0 10px;
        }
        
        .dev-terminal-content {
            margin-top: 30px;
            padding: 10px;
            height: calc(100% - 40px);
            overflow: auto;
        }
        
        .terminal-header {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 30px;
            display: flex;
            align-items: center;
            padding: 0 10px;
            z-index: 10;
        }
        
        .terminal-button {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .terminal-button-red {
            background-color: #ff5f56;
        }
        
        .terminal-button-yellow {
            background-color: #ffbd2e;
        }
        
        .terminal-button-green {
            background-color: #27c93f;
        }
        
        .terminal-title {
            margin-left: 10px;
            font-size: 13px;
            font-weight: 500;
            color: #8b949e;
        }
        
        .term-line {
            margin: 0;
            padding: 4px 0;
            line-height: 1.4;
            white-space: pre-wrap;
            word-break: break-all;
            display: flex;
        }
        
        .command-line {
            display: flex;
            align-items: center;
            margin: 6px 0;
        }
        
        .prompt {
            color: #58a6ff;
            margin-right: 8px;
            font-weight: bold;
        }
        
        .command-input {
            flex: 1;
            background: transparent;
            border: none;
            color: #e6edf3;
            font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
            font-size: 14px;
            padding: 0;
            outline: none;
        }
        
        .output-text {
            color: #e6edf3;
            padding-left: 0;
        }
        
        .output-error {
            color: #f85149;
        }
        
        .output-success {
            color: #56d364;
        }
        
        .output-warning {
            color: #e3b341;
        }
        
        .output-info {
            color: #58a6ff;
        }
        
        .blink {
            animation: terminal-blink 1s step-end infinite;
        }
        
        @keyframes terminal-blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        
        /* Command history and suggestion styles */
        .history-item {
            margin: 2px 0;
            padding: 4px 8px;
            cursor: pointer;
            border-radius: 4px;
            color: #8b949e;
        }
        
        .history-item:hover {
            background-color: #161b22;
            color: #e6edf3;
        }
        
        /* Dashboard elements */
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        
        .dashboard-card {
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .dashboard-card-header {
            font-size: 16px;
            font-weight: 500;
            color: #8b949e;
            margin-bottom: 10px;
            border-bottom: 1px solid #30363d;
            padding-bottom: 8px;
        }
        
        .dashboard-metric {
            font-size: 28px;
            font-weight: bold;
            color: #58a6ff;
            margin: 10px 0;
        }
        
        .dashboard-label {
            font-size: 13px;
            color: #8b949e;
        }
        
        .progress-bar {
            height: 6px;
            background-color: #0d1117;
            border-radius: 3px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .progress-value {
            height: 100%;
            background-color: #58a6ff;
            border-radius: 3px;
            transition: width 0.3s ease;
        }
        
        .pulse-animation {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        /* VOTSai header styles */
        .votsai-header {
            font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
            background-color: #0d1117;
            color: #e6edf3;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #30363d;
            text-align: center;
            margin-bottom: 15px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        }
        
        .votsai-link {
            display: inline-block;
            background-color: #161b22;
            color: #58a6ff !important;
            text-decoration: none;
            font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
            padding: 8px 16px;
            border-radius: 6px;
            border: 1px solid #30363d;
            transition: all 0.2s;
            font-size: 14px;
            margin-top: 10px;
        }
        
        .votsai-link:hover {
            background-color: #1f2937;
            border-color: #58a6ff;
            box-shadow: 0 0 10px rgba(88, 166, 255, 0.3);
        }
        
        /* Typing animation */
        .typing::after {
            content: '|';
            animation: cursor 1s infinite step-end;
        }
        
        @keyframes cursor {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        </style>
        """, unsafe_allow_html=True)
    
    def display(self, text, typing_effect=True, typing_speed=10, cascading_chars=True):
        """Display text in the Matrix terminal with effects"""
        # Make sure we're initialized
        if not self.initialized:
            self.initialize()
        
        # Create a placeholder for the terminal
        terminal_placeholder = st.empty()
        
        # Prepare HTML container
        terminal_html = f'<div class="matrix-terminal" id="matrix-terminal">'
        
        if typing_effect:
            # Display with typing effect
            full_text = ""
            lines = text.split('\n')
            
            # Update the terminal with typing effect
            for line in lines:
                # Add prefix to each line
                line_with_prefix = f'<span class="matrix-prefix">[SYSTEM]></span> {html.escape(line)}'
                full_text += f'<p class="matrix-line">{line_with_prefix}</p>'
                
                # Update the display
                terminal_html_with_content = terminal_html + full_text + '</div>'
                terminal_placeholder.markdown(terminal_html_with_content, unsafe_allow_html=True)
                
                # Pause for typing effect
                time.sleep(len(line) / typing_speed)
        else:
            # Display all at once
            for line in text.split('\n'):
                line_with_prefix = f'<span class="matrix-prefix">[SYSTEM]></span> {html.escape(line)}'
                terminal_html += f'<p class="matrix-line">{line_with_prefix}</p>'
            
            terminal_html += '</div>'
            terminal_placeholder.markdown(terminal_html, unsafe_allow_html=True)
        
        # Add cascading characters effect if requested
        if cascading_chars:
            self._add_cascading_effect(terminal_placeholder)
    
    def _add_cascading_effect(self, placeholder):
        """Add the Matrix cascading characters effect with orange color"""
        # JavaScript for cascading characters
        js_code = """
        <script>
        function createMatrixEffect() {
            const terminal = document.getElementById('matrix-terminal');
            const canvas = document.createElement('canvas');
            canvas.style.position = 'absolute';
            canvas.style.top = '0';
            canvas.style.left = '0';
            canvas.style.pointerEvents = 'none';
            canvas.style.zIndex = '-1';
            canvas.width = terminal.offsetWidth;
            canvas.height = terminal.offsetHeight;
            terminal.style.position = 'relative';
            terminal.appendChild(canvas);
            
            const ctx = canvas.getContext('2d');
            const characters = "日ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍｦｲｸｺｿﾁﾄﾉﾌﾔﾖﾙﾚﾛﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
            const fontSize = 14;
            const columns = Math.floor(canvas.width / fontSize);
            
            const drops = [];
            for (let i = 0; i < columns; i++) {
                drops[i] = Math.floor(Math.random() * -canvas.height / fontSize);
            }
            
            function draw() {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';  /* Reduced opacity for softer effect */
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                for (let i = 0; i < drops.length; i++) {
                    // Orange with varied brightness, less bright overall
                    const brightness = Math.floor(Math.random() * 20) + 50;
                    ctx.fillStyle = `rgba(${brightness + 155}, ${brightness + 40}, 0, 0.6)`;
                    
                    const text = characters[Math.floor(Math.random() * characters.length)];
                    ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                    
                    if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                        drops[i] = 0;
                    }
                    drops[i]++;
                }
            }
            
            setInterval(draw, 33);
        }
        
        // Initialize the effect when the DOM is loaded
        document.addEventListener('DOMContentLoaded', createMatrixEffect);
        // Also try to initialize right away
        setTimeout(createMatrixEffect, 500);
        </script>
        """
        placeholder.markdown(js_code, unsafe_allow_html=True)

    def splash_screen(self):
        """Display a Matrix splash screen animation"""
        placeholder = st.empty()
        
        # Matrix ASCII art
        matrix_ascii = """
        TTTTTTTTTTTTTTTTTTTTTHHHHHHHHH     HHHHHHHHHEEEEEEEEEEEEEEEEEEEEEE     MMMMMMMM               MMMMMMMM               AAA               TTTTTTTTTTTTTTTTTTTTTRRRRRRRRRRRRRRRRR   IIIIIIIIIXXXXXXXXXXX       XXXXXXXX
        T:::::::::::::::::::::TH:::::::H     H:::::::HE::::::::::::::::::::E     M:::::::M             M:::::::M              A:::A              T:::::::::::::::::::::TR::::::::::::::::R  I::::::::IX:::::::::X       X:::::X
        T:::::::::::::::::::::TH:::::::H     H:::::::HE::::::::::::::::::::E     M::::::::M           M::::::::M             A:::::A             T:::::::::::::::::::::TR::::::RRRRRR:::::R I::::::::IX:::::::::X       X:::::X
        T:::::TT:::::::TT:::::THH::::::H     H::::::HHEE::::::EEEEEEEEE::::E     M:::::::::M         M:::::::::M            A:::::::A            T:::::TT:::::::TT:::::TRR:::::R     R:::::RII::::::IIX::::::X:::::X   X:::::X
        TTTTTT  T:::::T  TTTTTT  H:::::H     H:::::H    E:::::E       EEEEEE     M::::::::::M       M::::::::::M           A:::::::::A           TTTTTT  T:::::T  TTTTTT  R::::R     R:::::R  I::::I  XXX:::::X:::::X X:::::XXX
                T:::::T          H:::::H     H:::::H    E:::::E                  M:::::::::::M     M:::::::::::M          A:::::A:::::A                  T:::::T          R::::R     R:::::R  I::::I     X:::::X:::::X:::::X   
                T:::::T          H::::::HHHHH::::::H    E::::::EEEEEEEEEE        M:::::::M::::M   M::::M:::::::M         A:::::A   A:::::A                 T:::::T          R::::RRRRRR:::::R   I::::I      X:::::X:::::::::X    
                T:::::T          H:::::::::::::::::H    E:::::::::::::::E        M::::::M M::::M M::::M M::::::M        A:::::A     A:::::A                T:::::T          R:::::::::::::RR    I::::I       X:::::X:::::::X     
                T:::::T          H:::::::::::::::::H    E:::::::::::::::E        M::::::M  M::::M::::M  M::::::M       A:::::A     A:::::A               T:::::T          R::::RRRRRR:::::R   I::::I       X:::::X:::::::X     
                T:::::T          H::::::HHHHH::::::H    E::::::EEEEEEEEEE        M::::::M   M:::::::M   M::::::M      A:::::AAAAAAAAA:::::A              T:::::T          R::::R     R:::::R  I::::I      X:::::X:::::::::X    
                T:::::T          H:::::H     H:::::H    E:::::E                  M::::::M    M:::::M    M::::::M     A:::::::::::::::::::::A             T:::::T          R::::R     R:::::R  I::::I     X:::::X:::::X:::::X   
                T:::::T          H:::::H     H:::::H    E:::::E       EEEEEE     M::::::M     MMMMM     M::::::M    A:::::AAAAAAAAAAAAA:::::A            T:::::T          R::::R     R:::::R  I::::I  XXX:::::X:::::X X:::::XXX
              TT:::::::TT      HH::::::H     H::::::HHEE::::::EEEEEEEE:::::E     M::::::M               M::::::M   A:::::A             A:::::A         TT:::::::TT      RR:::::R     R:::::RII::::::IIX::::::X:::::X   X:::::X
              T:::::::::T      H:::::::H     H:::::::HE::::::::::::::::::::E     M::::::M               M::::::M  A:::::A               A:::::A        T:::::::::T      R::::::R     R:::::RI::::::::IX:::::::::X       X:::::X
              T:::::::::T      H:::::::H     H:::::::HE::::::::::::::::::::E     M::::::M               M::::::M A:::::A                 A:::::A       T:::::::::T      R::::::R     R:::::RI::::::::IX:::::::::X       X:::::X
              TTTTTTTTTTT      HHHHHHHHH     HHHHHHHHHEEEEEEEEEEEEEEEEEEEEEEE    MMMMMMMM               MMMMMMMMAAAAAAA                   AAAAAAA      TTTTTTTTTTT      RRRRRRRR     RRRRRRRIIIIIIIIIIXXXXXXXX         XXXXXXX    
        """
        
        # Display the ASCII art letter by letter with a green typing effect
        html_content = '<div style="font-family: monospace; color: #00FF00; background-color: #000; padding: 20px; text-align: center; font-size: 10px; white-space: pre; animation: glow 1.5s ease-in-out infinite alternate;">'
        
        # Add letters one by one
        for i in range(len(matrix_ascii) + 1):
            current_text = matrix_ascii[:i]
            placeholder.markdown(html_content + current_text + '</div>', unsafe_allow_html=True)
            # Speed up display a bit for better UX
            if i % 50 == 0:  # Only update every 50 chars for performance
                time.sleep(0.01)
        
        time.sleep(1)  # Pause to show full logo
        
        # Dissolve effect
        for opacity in [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]:
            html_content = f'<div style="font-family: monospace; color: #00FF00; background-color: #000; padding: 20px; text-align: center; font-size: 10px; white-space: pre; opacity: {opacity};">'
            placeholder.markdown(html_content + matrix_ascii + '</div>', unsafe_allow_html=True)
            time.sleep(0.1)
        
        # Welcome message
        welcome_html = '<div style="font-family: monospace; color: #00FF00; background-color: #000; padding: 20px; text-align: center;">'
        welcome_html += '<h1 style="color: #00FF00; text-shadow: 0 0 10px #00FF00;">WELCOME TO THE MATRIX</h1>'
        welcome_html += '<p>The TRILOGY Brain is now online.</p>'
        welcome_html += '<p style="margin-top: 20px; font-size: 14px;">Enter your query to begin...</p>'
        welcome_html += '</div>'
        
        placeholder.markdown(welcome_html, unsafe_allow_html=True)
        time.sleep(2)
        placeholder.empty()

    def display_votsai_header(self):
        """Display VOTSai ASCII art and Village of Thousands link with better animation"""
        # Make sure we're initialized
        if not self.initialized:
            self.initialize()
        
        # Simplified VOTSai logo for better display
        votsai_ascii = r"""
  ____    ____  _______  _______   _____            _ 
 |_   \  /   _||_   __ \|_   __ \ / ___ `.         (_)
   |   \/   |    | |__) | | |__) |_/___) |   .--.   _ 
   | |\  /| |    |  ___/  |  __ / .'____.'  ( (`\] | |
  _| |_\/_| |_  _| |_    _| |  \ \ (____    `'.'.  | |
 |_____||_____||_____|  |____| |__)\____.> [\__) )(_)
    """
        
        # Display the ASCII art with professional styling
        st.markdown(f"""
        <div style="font-family: 'Consolas', 'Menlo', 'Monaco', monospace; 
            background-color: #242424; color: #e6e6e6; 
            padding: 15px; margin-bottom: 20px; white-space: pre; 
            font-size: 13px; border: 1px solid #444; border-radius: 4px; text-align: center;">
        {votsai_ascii}
        </div>
        
        <div style="text-align: center; margin-bottom: 30px;">
            <a href="https://www.villageofthousands.io/" target="_blank" 
               id="vots-link"
               style="color: #4c8daa; text-decoration: none; 
               font-family: 'Consolas', 'Menlo', 'Monaco', monospace; 
               background-color: #2b2b2b; display: inline-block;
               border: 1px solid #444; padding: 8px 16px; border-radius: 3px;">
               Powered by Village of Thousands
            </a>
        </div>
        
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            // Create typing animation for the link
            const link = document.getElementById('vots-link');
            const originalText = link.textContent.trim();
            
            // Typing animation
            const animateText = () => {{
                let i = 0;
                link.textContent = '';
                const interval = setInterval(() => {{
                    if (i < originalText.length) {{
                        link.textContent += originalText.charAt(i);
                        i++;
                    }} else {{
                        clearInterval(interval);
                        
                        // Add subtle transition effect 
                        link.style.transition = 'all 0.3s ease';
                        
                        // Add hover effect
                        link.addEventListener('mouseover', () => {{
                            link.style.backgroundColor = '#333';
                            link.style.borderColor = '#555';
                        }});
                        
                        link.addEventListener('mouseout', () => {{
                            link.style.backgroundColor = '#2b2b2b';
                            link.style.borderColor = '#444';
                        }});
                    }}
                }}, 40);
            }};
            
            // Start animation with a slight delay
            setTimeout(animateText, 300);
        }});
        </script>
        """, unsafe_allow_html=True)

    def display_modern_terminal(self, command, output, terminal_title="TRILOGY Brain Terminal"):
        """Display a modern developer terminal with command and output"""
        # Make sure we're initialized
        if not self.initialized:
            self.initialize()
        
        # Create a placeholder for the terminal
        terminal_placeholder = st.empty()
        
        # Prepare HTML container
        terminal_html = f'''
        <div class="dev-terminal">
            <div class="terminal-header">
                <div class="terminal-button terminal-button-red"></div>
                <div class="terminal-button terminal-button-yellow"></div>
                <div class="terminal-button terminal-button-green"></div>
                <div class="terminal-title">{terminal_title}</div>
            </div>
            <div class="dev-terminal-content">
        '''
        
        # Add command with typing effect
        terminal_html += f'''
            <div class="command-line">
                <span class="prompt">$ </span>
                <span class="command-input typing" id="command">{command}</span>
            </div>
        '''
        
        # Add spinning animation for loading
        terminal_html += '''
            <div class="term-line">
                <span class="output-text pulse-animation">Processing query... ⏳</span>
            </div>
        '''
        
        # Close the container
        terminal_html += '</div></div>'
        
        # Display initial terminal
        terminal_placeholder.markdown(terminal_html, unsafe_allow_html=True)
        
        # Wait a moment
        time.sleep(1)
        
        # Process output with typing effect
        lines = output.split('\n')
        
        for i, line in enumerate(lines):
            # Update terminal content with new line
            terminal_html = f'''
            <div class="dev-terminal">
                <div class="terminal-header">
                    <div class="terminal-button terminal-button-red"></div>
                    <div class="terminal-button terminal-button-yellow"></div>
                    <div class="terminal-button terminal-button-green"></div>
                    <div class="terminal-title">{terminal_title}</div>
                </div>
                <div class="dev-terminal-content">
                    <div class="command-line">
                        <span class="prompt">$ </span>
                        <span class="command-input">{command}</span>
                    </div>
            '''
            
            # Add processed lines
            for j in range(i + 1):
                line_class = "output-text"
                if lines[j].startswith("ERROR:"):
                    line_class = "output-error"
                elif lines[j].startswith("SUCCESS:"):
                    line_class = "output-success"
                elif lines[j].startswith("WARNING:"):
                    line_class = "output-warning"
                elif lines[j].startswith("[INFO]") or lines[j].startswith("INFO:"):
                    line_class = "output-info"
                    
                terminal_html += f'''
                    <div class="term-line">
                        <span class="{line_class}">{html.escape(lines[j])}</span>
                    </div>
                '''
            
            # Close container
            terminal_html += '</div></div>'
            
            # Update the display
            terminal_placeholder.markdown(terminal_html, unsafe_allow_html=True)
            
            # Add delay for typing effect (only for first few lines or long output)
            if i < 10 or len(lines) < 30:
                time.sleep(0.05)
        
        # Add command prompt at the end
        terminal_html += '''
            <div class="command-line">
                <span class="prompt">$ </span>
                <span class="command-input blink"></span>
            </div>
        '''
        
        terminal_placeholder.markdown(terminal_html, unsafe_allow_html=True)

    def display_dashboard_header(self):
        """Display a modern dashboard header with VOTSai branding and stats"""
        # Make sure we're initialized
        if not self.initialized:
            self.initialize()
        
        # VOTSai ASCII art
        votsai_ascii = r"""
__      _______ _______ _____ _____ 
\ \    / / ____|__   __/ ____|_   _|
 \ \  / / |  __   | | | (___   | |  
  \ \/ /| | |_ |  | |  \___ \  | |  
   \  / | |__| |  | |  ____) |_| |_ 
    \/   \_____|  |_| |_____/|_____|
    """
        
        # Display modern header with VOTSai branding
        st.markdown(f"""
        <div class="votsai-header">
            <pre style="font-size: 12px; line-height: 1.2;">{votsai_ascii}</pre>
            <h2 style="margin-top: 10px; color: #58a6ff;">TRILOGY Brain Terminal</h2>
            <p style="color: #8b949e; margin-bottom: 15px;">Advanced AI Orchestration System</p>
            <a href="https://www.villageofthousands.io/" target="_blank" class="votsai-link">
                Powered by Village of Thousands
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Create dashboard metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="dashboard-card">
                <div class="dashboard-card-header">System Status</div>
                <div class="dashboard-metric">Online</div>
                <div class="dashboard-label">All systems nominal</div>
                <div class="progress-bar">
                    <div class="progress-value" style="width: 98%; background-color: #56d364;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="dashboard-card">
                <div class="dashboard-card-header">Active Models</div>
                <div class="dashboard-metric">4</div>
                <div class="dashboard-label">Claude, DeepSeek, Perplexity, Local</div>
                <div class="progress-bar">
                    <div class="progress-value" style="width: 75%; background-color: #58a6ff;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="dashboard-card">
                <div class="dashboard-card-header">API Usage</div>
                <div class="dashboard-metric">68%</div>
                <div class="dashboard-label">Monthly quota remaining</div>
                <div class="progress-bar">
                    <div class="progress-value" style="width: 68%; background-color: #e3b341;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)