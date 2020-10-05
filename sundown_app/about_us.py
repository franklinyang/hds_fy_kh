import dash
import dash_core_components as dcc
import dash_html_components as html

about_us_html = html.Div(
    [
        html.H1("About us"),
        html.P(
            """
            This contains a map of the United States that examines Sundown towns. Sundown towns were towns,
            cities, and municipalities in the United States with anecdoatal evidence of systemic racism.\n
            """
        ),
        html.P(
            """
            This website embodies the work from a Capstone project from a data sciene masters program at the Harvard Chan School of Public Health.
            Participants were Kexin Huang and Franklin Yang, advised by Yulin Hwsen and Heather Mattie. \n
            """
        ),
        html.P(
            """
            This map was created using data collected from a Sundown Town project completed at Tougaloo college: https://sundown.tougaloo.edu/.
            """
        ),
    ]
)
