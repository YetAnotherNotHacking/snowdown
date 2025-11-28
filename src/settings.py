class SDSettings:
    appname = "SnowDown"
    company = "SilverFlag"
    version = "v0.1.1"
    name = "Admin"
    mail_server = "mail.silverflag.net"
    mail_user = "systemstatus@silverflag.net"
    mail_passphrase = "redacted for commit"
    mail_target = "dread@silverflag.net"
    mail_port = 465
    ntfy_endpoint = "https://ntfy.sh/silverflagsystemstatus"
    ntfy_title = "SnowDown Alert"
    def build_email_body(name, servername, timestamp, failreason):
        return f"""
        Hello {name},

        This is an automated message from a SnowDown daemon running on one of your servers.
        You are recieving this report because {servername} failed with reason {failreason}.
        This even occured at around {timestamp}.

        Goodbye.
        """
    def build_email_heading(servername, failreason):
        return f"ALERT: SnowDown- {servername} | {failreason}"
    def build_notification_content(servername, failreason):
        return f"{servername} is failing with the {failreason} error."