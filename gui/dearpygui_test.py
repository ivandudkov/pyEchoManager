import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(tag="Primary Window"):
    dpg.add_text("Hello, world")
    dpg.add_button(enabled=True, label="Press me", tag="item")
    # at a later time, change the item's configuration
    dpg.configure_item("item", enabled=False, label="New Label")

    with dpg.menu_bar():
        with dpg.menu(label="Main"):
            dpg.add_menu_item(label="Open")
            dpg.add_menu_item(label="Exit")

dpg.create_viewport(title='PyEchoManager. Fileset', width=800, height=600)
dpg.set_primary_window("Primary Window", True)
# must be called before showing viewport. Icons for viewport window
# dpg.set_viewport_small_icon("path/to/icon.ico")
# dpg.set_viewport_large_icon("path/to/icon.ico")

# dpg.show_style_editor()  # Style editor window
# dpg.show_metrics()  # Metrics and perormance monitor window

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()