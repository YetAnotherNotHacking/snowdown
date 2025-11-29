import json
from pathlib import Path
import urwid

# find out where the program should be storing it's configurations
def app_paths(app="snowdown"):
    cfg = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / app
    data = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share")) / app
    cfg.mkdir(parents=True, exist_ok=True)
    data.mkdir(parents=True, exist_ok=True)
    return cfg, data

class SDSettings:
    appname = "SnowDown" # not user edittable
    company = "SilverFlag" # not user edittable
    version = "v0.1.1" # not user edittable
    name = "Admin"
    mail_server = "mail.domain.com"
    mail_user = "email@domain.com"
    mail_passphrase = ""
    mail_target = "your@email.com"
    mail_port = 465
    ntfy_endpoint = "https://ntfy.sh/yourendpointhere"
    ntfy_title = "SnowDown"

    config_file = Path("sdsettings.json")

    @classmethod
    def setup(cls, *, name=None, mail_server=None, mail_user=None,
              mail_passphrase=None, mail_target=None, mail_port=None,
              ntfy_endpoint=None, ntfy_title=None):
        if name: cls.name = name
        if mail_server: cls.mail_server = mail_server
        if mail_user: cls.mail_user = mail_user
        if mail_passphrase: cls.mail_passphrase = mail_passphrase
        if mail_target: cls.mail_target = mail_target
        if mail_port: cls.mail_port = mail_port
        if ntfy_endpoint: cls.ntfy_endpoint = ntfy_endpoint
        if ntfy_title: cls.ntfy_title = ntfy_title
        cls.save_config()

    @classmethod
    def save_config(cls):
        data = {
            "name": cls.name,
            "mail_server": cls.mail_server,
            "mail_user": cls.mail_user,
            "mail_passphrase": cls.mail_passphrase,
            "mail_target": cls.mail_target,
            "mail_port": cls.mail_port,
            "ntfy_endpoint": cls.ntfy_endpoint,
            "ntfy_title": cls.ntfy_title
        }
        cls.config_file.write_text(json.dumps(data, indent=4))

    @classmethod
    def load_config(cls):
        if cls.config_file.exists():
            data = json.loads(cls.config_file.read_text())
            for key, value in data.items():
                setattr(cls, key, value)

    # maybe later find a way to make these edittable from the config, but how with illiterals?
    @staticmethod
    def build_email_body(name, servername, timestamp, failreason):
        return f"""
        Hello {name},

        This is an automated message from a SnowDown daemon running on one of your servers.
        You are recieving this report because {servername} failed with reason {failreason}.
        This even occured at around {timestamp}.

        Goodbye.
        """

    @staticmethod
    def build_email_heading(servername, failreason):
        return f"ALERT: SnowDown- {servername} | {failreason}"

    @staticmethod
    def build_notification_content(servername, failreason):
        return f"{servername} is failing with the {failreason} error."
# simple ui for users to be able to enter information, a basic lil table
def run_setup_tui():
    palette = [
        ("bg", "light gray", "black"),
        ("edit", "white", "dark blue"),
        ("edit_focus", "black", "yellow"),
        ("button", "black", "light gray"),
        ("button_focus", "white", "dark red"),
        ("label", "light cyan", "black"),
    ]

    fields = [
        "name",
        "mail_server",
        "mail_user",
        "mail_passphrase",
        "mail_target",
        "mail_port",
        "ntfy_endpoint",
        "ntfy_title"
    ]

    edits = {}
    widgets = []


    for k in fields:
        default = str(getattr(SDSettings, k))
        e = urwid.AttrMap(urwid.Edit(f"{k}: ", default), "edit", "edit_focus")
        edits[k] = e
        widgets.append(e)

    save_button = urwid.AttrMap(urwid.Button("Save"), "button", "button_focus")


    def done(button):
        vals = {}
        for k in fields:
            v = edits[k].original_widget.edit_text
            if k == "mail_port":
                v = int(v)
            vals[k] = v
        SDSettings.setup(**vals)
        raise urwid.ExitMainLoop()

    urwid.connect_signal(save_button.original_widget, "click", done)

    window = urwid.LineBox(
        urwid.Pile(widgets + [urwid.Divider(), save_button]),
        title="Setup"
    )
    ui = urwid.Filler(urwid.AttrMap(window, "bg"), valign="top")
    urwid.MainLoop(ui, palette).run()


# if being ran directly
if __name__ == "__main__":
    run_setup_tui()