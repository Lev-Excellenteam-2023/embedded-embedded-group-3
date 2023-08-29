# region email template
EMAIL_SUBJECT = "Fire Alert Notification"
STYLE_TEMPLATE = """
        <html>
          <head>
            <style>
              body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f2f2f2;
              }}
              .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
              }}
              .header {{
                text-align: center;
                margin-bottom: 20px;
              }}
              .coordinates {{
                font-weight: bold;
              }}
              .image-container {{
                text-align: center;
                margin-top: 20px;
              }}
              .image {{
                max-width: 100%;
                height: auto;
              }}
              .footer {{
                text-align: center;
                margin-top: 20px;
                color: #888;
              }}
            </style>
          </head> """

TEMPLATE_BODY_HEADER = """
        <body>
            <div class="container">
              <div class="header">
                <h1>Fire Alert Notification</h1>
              </div>
              <p>A fire has been detected at the following location:</p>"""

TEMPLATE_BODY_FOOTER = """
            <p>Please find the attached image for reference.</p>
            </div>
              <div class="footer">
                <p>Regards<br>Wild Fire Warning System</p>
              </div>
            </div>
          </body>
        </html>"""

# endregion

# region image extensions
PNG = ".png"
JPG = ".jpg"

# endregion
