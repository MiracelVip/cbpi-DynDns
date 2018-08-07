from modules import cbpi, 

@cbpi.backgroundtask(key="my_task", interval=1)
def my_custom_background_task():
    # YOUR CODE GOES HERE
    pass

# Add Config Parameter        
@cbpi.initalizer(order=0)
def initDynDns(app):

    api_url = app.get_config_parameter("DynDns_API_Url",None)
    if api_url is None:
        api_url = "https://dynv6.com/api/update"
        cbpi.add_config_parameter("DynDns_API_Url", "https://dynv6.com/api/update", "text", "The update URL to be called")

    domainname = app.get_config_parameter("DynDns_Domainname", None)
    if domainname is None:
        domainname = "yourDynName.dynv6.net"
        cbpi.add_config_parameter("DynDns_Domainname", "yourDynName.dynv6.net", "text", "Your dynamic adress")

    api_token = app.get_config_parameter("DynDns_API_token", None)
    if api_token is None:
        api_token = "000000000"
        cbpi.add_config_parameter("DynDns_API_token", "000000000", "text", "Your API token")

    version = app.get_config_parameter("DynDns_IP_Version", None)
    if version is None:
        version = "4&6"
        cbpi.add_config_parameter("DynDns_Ip_Version", "4 & 6", "select", "MQTT password", ["4", "6", "4 & 6"])
