# system_monitor_dash

## Classes

### Dash

Dash is a framework for building analytical web applications.
    No JavaScript required.

    If a parameter can be set by an environment variable, that is listed as:
        env: ``DASH_****``
    Values provided here take precedence over environment variables.

    :param name: The name Flask should use for your app. Even if you provide
        your own ``server``, ``name`` will be used to help find assets.
        Typically ``__name__`` (the magic global var, not a string) is the
        best value to use. Default ``'__main__'``, env: ``DASH_APP_NAME``
    :type name: string

    :param server: Sets the Flask server for your app. There are three options:
        ``True`` (default): Dash will create a new server
        ``False``: The server will be added later via ``app.init_app(server)``
            where ``server`` is a ``flask.Flask`` instance.
        ``flask.Flask``: use this pre-existing Flask server.
    :type server: boolean or flask.Flask

    :param assets_folder: a path, relative to the current working directory,
        for extra files to be used in the browser. Default ``'assets'``.
        All .js and .css files will be loaded immediately unless excluded by
        ``assets_ignore``, and other files such as images will be served if
        requested.
    :type assets_folder: string

    :param pages_folder: a relative or absolute path for pages of a multi-page app.
        Default ``'pages'``.
    :type pages_folder: string or pathlib.Path

    :param use_pages: When True, the ``pages`` feature for multi-page apps is
        enabled. If you set a non-default ``pages_folder`` this will be inferred
        to be True. Default `None`.
    :type use_pages: boolean

    :param include_pages_meta: Include the page meta tags for twitter cards.
    :type include_pages_meta: bool

    :param assets_url_path: The local urls for assets will be:
        ``requests_pathname_prefix + assets_url_path + '/' + asset_path``
        where ``asset_path`` is the path to a file inside ``assets_folder``.
        Default ``'assets'``.
    :type asset_url_path: string

    :param assets_ignore: A regex, as a string to pass to ``re.compile``, for
        assets to omit from immediate loading. Ignored files will still be
        served if specifically requested. You cannot use this to prevent access
        to sensitive files.
    :type assets_ignore: string

    :param assets_external_path: an absolute URL from which to load assets.
        Use with ``serve_locally=False``. assets_external_path is joined
        with assets_url_path to determine the absolute url to the
        asset folder. Dash can still find js and css to automatically load
        if you also keep local copies in your assets folder that Dash can index,
        but external serving can improve performance and reduce load on
        the Dash server.
        env: ``DASH_ASSETS_EXTERNAL_PATH``
    :type assets_external_path: string

    :param include_assets_files: Default ``True``, set to ``False`` to prevent
        immediate loading of any assets. Assets will still be served if
        specifically requested. You cannot use this to prevent access
        to sensitive files. env: ``DASH_INCLUDE_ASSETS_FILES``
    :type include_assets_files: boolean

    :param url_base_pathname: A local URL prefix to use app-wide.
        Default ``'/'``. Both `requests_pathname_prefix` and
        `routes_pathname_prefix` default to `url_base_pathname`.
        env: ``DASH_URL_BASE_PATHNAME``
    :type url_base_pathname: string

    :param requests_pathname_prefix: A local URL prefix for file requests.
        Defaults to `url_base_pathname`, and must end with
        `routes_pathname_prefix`. env: ``DASH_REQUESTS_PATHNAME_PREFIX``
    :type requests_pathname_prefix: string

    :param routes_pathname_prefix: A local URL prefix for JSON requests.
        Defaults to ``url_base_pathname``, and must start and end
        with ``'/'``. env: ``DASH_ROUTES_PATHNAME_PREFIX``
    :type routes_pathname_prefix: string

    :param serve_locally: If ``True`` (default), assets and dependencies
        (Dash and Component js and css) will be served from local URLs.
        If ``False`` we will use CDN links where available.
    :type serve_locally: boolean

    :param compress: Use gzip to compress files and data served by Flask.
        To use this option, you need to install dash[compress]
        Default ``False``
    :type compress: boolean

    :param meta_tags: html <meta> tags to be added to the index page.
        Each dict should have the attributes and values for one tag, eg:
        ``{'name': 'description', 'content': 'My App'}``
    :type meta_tags: list of dicts

    :param index_string: Override the standard Dash index page.
        Must contain the correct insertion markers to interpolate various
        content into it depending on the app config and components used.
        See https://dash.plotly.com/external-resources for details.
    :type index_string: string

    :param external_scripts: Additional JS files to load with the page.
        Each entry can be a string (the URL) or a dict with ``src`` (the URL)
        and optionally other ``<script>`` tag attributes such as ``integrity``
        and ``crossorigin``.
    :type external_scripts: list of strings or dicts

    :param external_stylesheets: Additional CSS files to load with the page.
        Each entry can be a string (the URL) or a dict with ``href`` (the URL)
        and optionally other ``<link>`` tag attributes such as ``rel``,
        ``integrity`` and ``crossorigin``.
    :type external_stylesheets: list of strings or dicts

    :param suppress_callback_exceptions: Default ``False``: check callbacks to
        ensure referenced IDs exist and props are valid. Set to ``True``
        if your layout is dynamic, to bypass these checks.
        env: ``DASH_SUPPRESS_CALLBACK_EXCEPTIONS``
    :type suppress_callback_exceptions: boolean

    :param prevent_initial_callbacks: Default ``False``: Sets the default value
        of ``prevent_initial_call`` for all callbacks added to the app.
        Normally all callbacks are fired when the associated outputs are first
        added to the page. You can disable this for individual callbacks by
        setting ``prevent_initial_call`` in their definitions, or set it
        ``True`` here in which case you must explicitly set it ``False`` for
        those callbacks you wish to have an initial call. This setting has no
        effect on triggering callbacks when their inputs change later on.

    :param show_undo_redo: Default ``False``, set to ``True`` to enable undo
        and redo buttons for stepping through the history of the app state.
    :type show_undo_redo: boolean

    :param extra_hot_reload_paths: A list of paths to watch for changes, in
        addition to assets and known Python and JS code, if hot reloading is
        enabled.
    :type extra_hot_reload_paths: list of strings

    :param plugins: Extend Dash functionality by passing a list of objects
        with a ``plug`` method, taking a single argument: this app, which will
        be called after the Flask server is attached.
    :type plugins: list of objects

    :param title: Default ``Dash``. Configures the document.title
    (the text that appears in a browser tab).

    :param update_title: Default ``Updating...``. Configures the document.title
    (the text that appears in a browser tab) text when a callback is being run.
    Set to None or '' if you don't want the document.title to change or if you
    want to control the document.title through a separate component or
    clientside callback.

    :param long_callback_manager: Deprecated, use ``background_callback_manager``
        instead.

    :param background_callback_manager: Background callback manager instance
        to support the ``@callback(..., background=True)`` decorator.
        One of ``DiskcacheManager`` or ``CeleryManager`` currently supported.

    :param add_log_handler: Automatically add a StreamHandler to the app logger
        if not added previously.

    :param hooks: Extend Dash renderer functionality by passing a dictionary of
    javascript functions. To hook into the layout, use dict keys "layout_pre" and
    "layout_post". To hook into the callbacks, use keys "request_pre" and "request_post"

    :param routing_callback_inputs: When using Dash pages (use_pages=True), allows to
    add new States to the routing callback, to pass additional data to the layout
    functions. The syntax for this parameter is a dict of State objects:
    `routing_callback_inputs={"language": Input("language", "value")}`
    NOTE: the keys "pathname_" and "search_" are reserved for internal use.

    :param description:  Sets a default description for meta tags on Dash pages (use_pages=True).

    :param on_error: Global callback error handler to call when
        an exception is raised. Receives the exception object as first argument.
        The callback_context can be used to access the original callback inputs,
        states and output.

#### Methods

##### __init__

```python
__init__(self, name: Optional[str] = None, server: Union[bool, flask.app.Flask] = True, assets_folder: str = 'assets', pages_folder: str = 'pages', use_pages: Optional[bool] = None, assets_url_path: str = 'assets', assets_ignore: str = '', assets_external_path: Optional[str] = None, eager_loading: bool = False, include_assets_files: bool = True, include_pages_meta: bool = True, url_base_pathname: Optional[str] = None, requests_pathname_prefix: Optional[str] = None, routes_pathname_prefix: Optional[str] = None, serve_locally: bool = True, compress: Optional[bool] = None, meta_tags: Optional[List[Dict[str, Any]]] = None, index_string: str = '<!DOCTYPE html>\n<html>\n    <head>\n        {%metas%}\n        <title>{%title%}</title>\n        {%favicon%}\n        {%css%}\n    </head>\n    <body>\n        <!--[if IE]><script>\n        alert("Dash v2.7+ does not support Internet Explorer. Please use a newer browser.");\n        </script><![endif]-->\n        {%app_entry%}\n        <footer>\n            {%config%}\n            {%scripts%}\n            {%renderer%}\n        </footer>\n    </body>\n</html>', external_scripts: Optional[List[Union[str, Dict[str, Any]]]] = None, external_stylesheets: Optional[List[Union[str, Dict[str, Any]]]] = None, suppress_callback_exceptions: Optional[bool] = None, prevent_initial_callbacks: bool = False, show_undo_redo: bool = False, extra_hot_reload_paths: Optional[List[str]] = None, plugins: Optional[list] = None, title: str = 'Dash', update_title: str = 'Updating...', long_callback_manager: Optional[Any] = None, background_callback_manager: Optional[Any] = None, add_log_handler: bool = True, hooks: Optional[dash.types.RendererHooks] = None, routing_callback_inputs: Optional[Dict[str, Union[dash.dependencies.Input, dash.dependencies.State]]] = None, description: Optional[str] = None, on_error: Optional[Callable[[Exception], Any]] = None, **obsolete)
```

##### add_startup_route

```python
add_startup_route(name, view_func, methods)
```

Add a route to the app to be initialized at the end of Dash initialization.
        Use this if the package requires a route to be added to the app, and you will not need to worry about at what point to add it.

        :param name: The name of the route. eg "my-new-url/path".
        :param view_func: The function to call when the route is requested. The function should return a JSON serializable object.
        :param methods: The HTTP methods that the route should respond to. eg ["GET", "POST"] or either one.

##### callback

```python
callback(self, *_args, **_kwargs)
```

Normally used as a decorator, `@app.callback` provides a server-side
        callback relating the values of one or more `Output` items to one or
        more `Input` items which will trigger the callback when they change,
        and optionally `State` items which provide additional information but
        do not trigger the callback directly.

        The last, optional argument `prevent_initial_call` causes the callback
        not to fire when its outputs are first added to the page. Defaults to
        `False` unless `prevent_initial_callbacks=True` at the app level.

##### clientside_callback

```python
clientside_callback(self, clientside_function, *args, **kwargs)
```

Create a callback that updates the output by calling a clientside
        (JavaScript) function instead of a Python function.

        Unlike `@app.callback`, `clientside_callback` is not a decorator:
        it takes either a
        `dash.dependencies.ClientsideFunction(namespace, function_name)`
        argument that describes which JavaScript function to call
        (Dash will look for the JavaScript function at
        `window.dash_clientside[namespace][function_name]`), or it may take
        a string argument that contains the clientside function source.

        For example, when using a `dash.dependencies.ClientsideFunction`:
        ```
        app.clientside_callback(
            ClientsideFunction('my_clientside_library', 'my_function'),
            Output('my-div' 'children'),
            [Input('my-input', 'value'),
             Input('another-input', 'value')]
        )
        ```

        With this signature, Dash's front-end will call
        `window.dash_clientside.my_clientside_library.my_function` with the
        current values of the `value` properties of the components `my-input`
        and `another-input` whenever those values change.

        Include a JavaScript file by including it your `assets/` folder. The
        file can be named anything but you'll need to assign the function's
        namespace to the `window.dash_clientside` namespace. For example,
        this file might look:
        ```
        window.dash_clientside = window.dash_clientside || {};
        window.dash_clientside.my_clientside_library = {
            my_function: function(input_value_1, input_value_2) {
                return (
                    parseFloat(input_value_1, 10) +
                    parseFloat(input_value_2, 10)
                );
            }
        }
        ```

        Alternatively, you can pass the JavaScript source directly to
        `clientside_callback`. In this case, the same example would look like:
        ```
        app.clientside_callback(
            '''
            function(input_value_1, input_value_2) {
                return (
                    parseFloat(input_value_1, 10) +
                    parseFloat(input_value_2, 10)
                );
            }
            ''',
            Output('my-div' 'children'),
            [Input('my-input', 'value'),
             Input('another-input', 'value')]
        )
        ```

        The last, optional argument `prevent_initial_call` causes the callback
        not to fire when its outputs are first added to the page. Defaults to
        `False` unless `prevent_initial_callbacks=True` at the app level.

##### csp_hashes

```python
csp_hashes(self, hash_algorithm='sha256')
```

Calculates CSP hashes (sha + base64) of all inline scripts, such that
        one of the biggest benefits of CSP (disallowing general inline scripts)
        can be utilized together with Dash clientside callbacks (inline scripts).

        Calculate these hashes after all inline callbacks are defined,
        and add them to your CSP headers before starting the server, for example
        with the flask-talisman package from PyPI:

        flask_talisman.Talisman(app.server, content_security_policy={
            "default-src": "'self'",
            "script-src": ["'self'"] + app.csp_hashes()
        })

        :param hash_algorithm: One of the recognized CSP hash algorithms ('sha256', 'sha384', 'sha512').
        :return: List of CSP hash strings of all inline scripts.

##### dependencies

```python
dependencies(self)
```

##### dispatch

```python
dispatch(self)
```

##### enable_dev_tools

```python
enable_dev_tools(self, debug=None, dev_tools_ui=None, dev_tools_props_check=None, dev_tools_serve_dev_bundles=None, dev_tools_hot_reload=None, dev_tools_hot_reload_interval=None, dev_tools_hot_reload_watch_interval=None, dev_tools_hot_reload_max_retry=None, dev_tools_silence_routes_logging=None, dev_tools_prune_errors=None)
```

Activate the dev tools, called by `run`. If your application
        is served by wsgi and you want to activate the dev tools, you can call
        this method out of `__main__`.

        All parameters can be set by environment variables as listed.
        Values provided here take precedence over environment variables.

        Available dev_tools environment variables:

            - DASH_DEBUG
            - DASH_UI
            - DASH_PROPS_CHECK
            - DASH_SERVE_DEV_BUNDLES
            - DASH_HOT_RELOAD
            - DASH_HOT_RELOAD_INTERVAL
            - DASH_HOT_RELOAD_WATCH_INTERVAL
            - DASH_HOT_RELOAD_MAX_RETRY
            - DASH_SILENCE_ROUTES_LOGGING
            - DASH_PRUNE_ERRORS

        :param debug: Enable/disable all the dev tools unless overridden by the
            arguments or environment variables. Default is ``True`` when
            ``enable_dev_tools`` is called directly, and ``False`` when called
            via ``run``. env: ``DASH_DEBUG``
        :type debug: bool

        :param dev_tools_ui: Show the dev tools UI. env: ``DASH_UI``
        :type dev_tools_ui: bool

        :param dev_tools_props_check: Validate the types and values of Dash
            component props. env: ``DASH_PROPS_CHECK``
        :type dev_tools_props_check: bool

        :param dev_tools_serve_dev_bundles: Serve the dev bundles. Production
            bundles do not necessarily include all the dev tools code.
            env: ``DASH_SERVE_DEV_BUNDLES``
        :type dev_tools_serve_dev_bundles: bool

        :param dev_tools_hot_reload: Activate hot reloading when app, assets,
            and component files change. env: ``DASH_HOT_RELOAD``
        :type dev_tools_hot_reload: bool

        :param dev_tools_hot_reload_interval: Interval in seconds for the
            client to request the reload hash. Default 3.
            env: ``DASH_HOT_RELOAD_INTERVAL``
        :type dev_tools_hot_reload_interval: float

        :param dev_tools_hot_reload_watch_interval: Interval in seconds for the
            server to check asset and component folders for changes.
            Default 0.5. env: ``DASH_HOT_RELOAD_WATCH_INTERVAL``
        :type dev_tools_hot_reload_watch_interval: float

        :param dev_tools_hot_reload_max_retry: Maximum number of failed reload
            hash requests before failing and displaying a pop up. Default 8.
            env: ``DASH_HOT_RELOAD_MAX_RETRY``
        :type dev_tools_hot_reload_max_retry: int

        :param dev_tools_silence_routes_logging: Silence the `werkzeug` logger,
            will remove all routes logging. Enabled with debugging by default
            because hot reload hash checks generate a lot of requests.
            env: ``DASH_SILENCE_ROUTES_LOGGING``
        :type dev_tools_silence_routes_logging: bool

        :param dev_tools_prune_errors: Reduce tracebacks to just user code,
            stripping out Flask and Dash pieces. Only available with debugging.
            `True` by default, set to `False` to see the complete traceback.
            env: ``DASH_PRUNE_ERRORS``
        :type dev_tools_prune_errors: bool

        :return: debug

##### enable_pages

```python
enable_pages(self)
```

##### get_asset_url

```python
get_asset_url(self, path)
```

##### get_dist

```python
get_dist(self, libraries)
```

##### get_relative_path

```python
get_relative_path(self, path)
```

Return a path with `requests_pathname_prefix` prefixed before it.
        Use this function when specifying local URL paths that will work
        in environments regardless of what `requests_pathname_prefix` is.
        In some deployment environments, like Dash Enterprise,
        `requests_pathname_prefix` is set to the application name,
        e.g. `my-dash-app`.
        When working locally, `requests_pathname_prefix` might be unset and
        so a relative URL like `/page-2` can just be `/page-2`.
        However, when the app is deployed to a URL like `/my-dash-app`, then
        `app.get_relative_path('/page-2')` will return `/my-dash-app/page-2`.
        This can be used as an alternative to `get_asset_url` as well with
        `app.get_relative_path('/assets/logo.png')`

        Use this function with `app.strip_relative_path` in callbacks that
        deal with `dcc.Location` `pathname` routing.
        That is, your usage may look like:
        ```
        app.layout = html.Div([
            dcc.Location(id='url'),
            html.Div(id='content')
        ])
        @app.callback(Output('content', 'children'), [Input('url', 'pathname')])
        def display_content(path):
            page_name = app.strip_relative_path(path)
            if not page_name:  # None or ''
                return html.Div([
                    dcc.Link(href=app.get_relative_path('/page-1')),
                    dcc.Link(href=app.get_relative_path('/page-2')),
                ])
            elif page_name == 'page-1':
                return chapters.page_1
            if page_name == "page-2":
                return chapters.page_2
        ```

##### index

```python
index(self, *args, **kwargs)
```

##### init_app

```python
init_app(self, app=None, **kwargs)
```

Initialize the parts of Dash that require a flask app.

##### interpolate_index

```python
interpolate_index(self, metas='', title='', css='', config='', scripts='', app_entry='', favicon='', renderer='')
```

Called to create the initial HTML string that is loaded on page.
        Override this method to provide you own custom HTML.

        :Example:

            class MyDash(dash.Dash):
                def interpolate_index(self, **kwargs):
                    return '''<!DOCTYPE html>
                    <html>
                        <head>
                            <title>My App</title>
                        </head>
                        <body>
                            <div id="custom-header">My custom header</div>
                            {app_entry}
                            {config}
                            {scripts}
                            {renderer}
                            <div id="custom-footer">My custom footer</div>
                        </body>
                    </html>'''.format(app_entry=kwargs.get('app_entry'),
                                      config=kwargs.get('config'),
                                      scripts=kwargs.get('scripts'),
                                      renderer=kwargs.get('renderer'))

        :param metas: Collected & formatted meta tags.
        :param title: The title of the app.
        :param css: Collected & formatted css dependencies as <link> tags.
        :param config: Configs needed by dash-renderer.
        :param scripts: Collected & formatted scripts tags.
        :param renderer: A script tag that instantiates the DashRenderer.
        :param app_entry: Where the app will render.
        :param favicon: A favicon <link> tag if found in assets folder.
        :return: The interpolated HTML string for the index.

##### long_callback

```python
long_callback(self, *_args, manager=None, interval=1000, running=None, cancel=None, progress=None, progress_default=None, cache_args_to_ignore=None, **_kwargs)
```

Deprecated: long callbacks are now supported natively with regular callbacks,
        use `background=True` with `dash.callback` or `app.callback` instead.

##### run

```python
run(self, host='127.0.0.1', port='8050', proxy=None, debug=None, jupyter_mode: Optional[Literal['inline', 'external', 'jupyterlab', 'tab', '_none']] = None, jupyter_width='100%', jupyter_height=650, jupyter_server_url=None, dev_tools_ui=None, dev_tools_props_check=None, dev_tools_serve_dev_bundles=None, dev_tools_hot_reload=None, dev_tools_hot_reload_interval=None, dev_tools_hot_reload_watch_interval=None, dev_tools_hot_reload_max_retry=None, dev_tools_silence_routes_logging=None, dev_tools_prune_errors=None, **flask_run_options)
```

Start the flask server in local mode, you should not run this on a
        production server, use gunicorn/waitress instead.

        If a parameter can be set by an environment variable, that is listed
        too. Values provided here take precedence over environment variables.

        :param host: Host IP used to serve the application
            env: ``HOST``
        :type host: string

        :param port: Port used to serve the application
            env: ``PORT``
        :type port: int

        :param proxy: If this application will be served to a different URL
            via a proxy configured outside of Python, you can list it here
            as a string of the form ``"{input}::{output}"``, for example:
            ``"http://0.0.0.0:8050::https://my.domain.com"``
            so that the startup message will display an accurate URL.
            env: ``DASH_PROXY``
        :type proxy: string

        :param debug: Set Flask debug mode and enable dev tools.
            env: ``DASH_DEBUG``
        :type debug: bool

        :param debug: Enable/disable all the dev tools unless overridden by the
            arguments or environment variables. Default is ``True`` when
            ``enable_dev_tools`` is called directly, and ``False`` when called
            via ``run``. env: ``DASH_DEBUG``
        :type debug: bool

        :param dev_tools_ui: Show the dev tools UI. env: ``DASH_UI``
        :type dev_tools_ui: bool

        :param dev_tools_props_check: Validate the types and values of Dash
            component props. env: ``DASH_PROPS_CHECK``
        :type dev_tools_props_check: bool

        :param dev_tools_serve_dev_bundles: Serve the dev bundles. Production
            bundles do not necessarily include all the dev tools code.
            env: ``DASH_SERVE_DEV_BUNDLES``
        :type dev_tools_serve_dev_bundles: bool

        :param dev_tools_hot_reload: Activate hot reloading when app, assets,
            and component files change. env: ``DASH_HOT_RELOAD``
        :type dev_tools_hot_reload: bool

        :param dev_tools_hot_reload_interval: Interval in seconds for the
            client to request the reload hash. Default 3.
            env: ``DASH_HOT_RELOAD_INTERVAL``
        :type dev_tools_hot_reload_interval: float

        :param dev_tools_hot_reload_watch_interval: Interval in seconds for the
            server to check asset and component folders for changes.
            Default 0.5. env: ``DASH_HOT_RELOAD_WATCH_INTERVAL``
        :type dev_tools_hot_reload_watch_interval: float

        :param dev_tools_hot_reload_max_retry: Maximum number of failed reload
            hash requests before failing and displaying a pop up. Default 8.
            env: ``DASH_HOT_RELOAD_MAX_RETRY``
        :type dev_tools_hot_reload_max_retry: int

        :param dev_tools_silence_routes_logging: Silence the `werkzeug` logger,
            will remove all routes logging. Enabled with debugging by default
            because hot reload hash checks generate a lot of requests.
            env: ``DASH_SILENCE_ROUTES_LOGGING``
        :type dev_tools_silence_routes_logging: bool

        :param dev_tools_prune_errors: Reduce tracebacks to just user code,
            stripping out Flask and Dash pieces. Only available with debugging.
            `True` by default, set to `False` to see the complete traceback.
            env: ``DASH_PRUNE_ERRORS``
        :type dev_tools_prune_errors: bool

        :param jupyter_mode: How to display the application when running
            inside a jupyter notebook.

        :param jupyter_width: Determine the width of the output cell
            when displaying inline in jupyter notebooks.
        :type jupyter_width: str

        :param jupyter_height: Height of app when displayed using
            jupyter_mode="inline"
        :type jupyter_height: int

        :param jupyter_server_url: Custom server url to display
            the app in jupyter notebook.

        :param flask_run_options: Given to `Flask.run`

        :return:

##### run_server

```python
run_server(self, *args, **kwargs)
```

`run_server` is a deprecated alias of `run` and may be removed in a
        future version. We recommend using `app.run` instead.

        See `app.run` for usage information.

##### serve_component_suites

```python
serve_component_suites(self, package_name, fingerprinted_path)
```

##### serve_layout

```python
serve_layout(self)
```

##### serve_reload_hash

```python
serve_reload_hash(self)
```

##### setup_startup_routes

```python
setup_startup_routes(self)
```

Initialize the startup routes stored in STARTUP_ROUTES.

##### strip_relative_path

```python
strip_relative_path(self, path)
```

Return a path with `requests_pathname_prefix` and leading and trailing
        slashes stripped from it. Also, if None is passed in, None is returned.
        Use this function with `get_relative_path` in callbacks that deal
        with `dcc.Location` `pathname` routing.
        That is, your usage may look like:
        ```
        app.layout = html.Div([
            dcc.Location(id='url'),
            html.Div(id='content')
        ])
        @app.callback(Output('content', 'children'), [Input('url', 'pathname')])
        def display_content(path):
            page_name = app.strip_relative_path(path)
            if not page_name:  # None or ''
                return html.Div([
                    dcc.Link(href=app.get_relative_path('/page-1')),
                    dcc.Link(href=app.get_relative_path('/page-2')),
                ])
            elif page_name == 'page-1':
                return chapters.page_1
            if page_name == "page-2":
                return chapters.page_2
        ```
        Note that `chapters.page_1` will be served if the user visits `/page-1`
        _or_ `/page-1/` since `strip_relative_path` removes the trailing slash.

        Also note that `strip_relative_path` is compatible with
        `get_relative_path` in environments where `requests_pathname_prefix` set.
        In some deployment environments, like Dash Enterprise,
        `requests_pathname_prefix` is set to the application name, e.g. `my-dash-app`.
        When working locally, `requests_pathname_prefix` might be unset and
        so a relative URL like `/page-2` can just be `/page-2`.
        However, when the app is deployed to a URL like `/my-dash-app`, then
        `app.get_relative_path('/page-2')` will return `/my-dash-app/page-2`

        The `pathname` property of `dcc.Location` will return '`/my-dash-app/page-2`'
        to the callback.
        In this case, `app.strip_relative_path('/my-dash-app/page-2')`
        will return `'page-2'`

        For nested URLs, slashes are still included:
        `app.strip_relative_path('/page-1/sub-page-1/')` will return
        `page-1/sub-page-1`
        ```

### Input

Input of callback: trigger an update when it is updated.

#### Methods

##### __init__

```python
__init__(self, component_id, component_property)
```

##### component_id_str

```python
component_id_str(self)
```

##### has_wildcard

```python
has_wildcard(self)
```

Return true if id contains a wildcard (MATCH, ALL, or ALLSMALLER)

##### to_dict

```python
to_dict(self)
```

### Output

Output of a callback.

#### Methods

##### __init__

```python
__init__(self, component_id, component_property, allow_duplicate=False)
```

##### component_id_str

```python
component_id_str(self)
```

##### has_wildcard

```python
has_wildcard(self)
```

Return true if id contains a wildcard (MATCH, ALL, or ALLSMALLER)

##### to_dict

```python
to_dict(self)
```

### datetime

datetime(year, month, day[, hour[, minute[, second[, microsecond[,tzinfo]]]]])

The year, month and day arguments are required. tzinfo may be None, or an
instance of a tzinfo subclass. The remaining arguments may be ints.

## Functions

### get_metrics

```python
get_metrics()
```

Fetch system metrics with error handling.

### toggle_logging

```python
toggle_logging(n_clicks)
```

### update_dashboard

```python
update_dashboard(n)
```

