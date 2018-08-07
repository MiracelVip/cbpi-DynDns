from modules import cbpi
from urllib2 import urlopen


@cbpi.backgroundtask(key="Update_DynDns", interval=600)
def update_DynDns(app):
    #''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Get IPv4
    #''''''''''''''''''''''''''''''''''''''''''''''''''''
    if app.get_config_parameter("DynDns_IP_Version", None) == "4" or app.get_config_parameter("DynDns_IP_Version", None) == "4 & 6":
        try:
            ipv4 = urlopen('https://v4.ident.me/', timeout = 10)
            ipv4 = ipv4.read()
        except:
            cbpi.notify('DynDns',"IPv4 Timeout - Please check your internet connection or configuration.", type = 'danger')
        
    #''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Get IPv6
    #''''''''''''''''''''''''''''''''''''''''''''''''''''    
    if app.get_config_parameter("DynDns_IP_Version", None) == "6" or app.get_config_parameter("DynDns_IP_Version", None) == "4 & 6":
        try:
            ipv6 = urlopen('https://v6.ident.me/', timeout = 10)
            ipv6 = ipv6.read()
        except:
            cbpi.notify('DynDns',"IPv6 Timeout - Please check your internet connection or configuration.", type = 'danger')
        
    #''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Build URL for update
    #''''''''''''''''''''''''''''''''''''''''''''''''''''    
    url = str(app.get_config_parameter("DynDns_API_Url", None)) + '?hostname=' + str(app.get_config_parameter("DynDns_Domainname", None)) + '&token=' + str(app.get_config_parameter("DynDns_API_token", None))
    
    if app.get_config_parameter("DynDns_IP_Version", None) == "4" or app.get_config_parameter("DynDns_IP_Version", None) == "4 & 6":
        url = str(url) + '&ipv4=' + str(ipv4)
        
    if app.get_config_parameter("DynDns_IP_Version", None) == "6" or app.get_config_parameter("DynDns_IP_Version", None) == "4 & 6":
        url = str(url) + '&ipv6=' + str(ipv6)
        
    #''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Update the IP
    #''''''''''''''''''''''''''''''''''''''''''''''''''''      
    try:
        update = urlopen(url, timeout = 10)
        update = update.read()
    except:
        cbpi.notify('DynDns',"Update failed - Please check your internet connection or configuration. " + url, type = 'danger', timeout=None)
        return
    
    print(update[:12]) #dynv6.com return "/n" 
    if update[:12] == "addresses un":
        cbpi.app.logger.info("DynDns - Adresses unchanged")
    elif update[:12] == "addresses up":
        cbpi.notify('DynDns',"DynDns updated", type = 'info')
        cbpi.app.logger.info("DynDns - Adresses updated")
    else:
        cbpi.notify('DynDns',update + url, type = 'danger', timeout= None)    



#''''''''''''''''''''''''''''''''''''''''''''''''''''
# Create parameter
#''''''''''''''''''''''''''''''''''''''''''''''''''''        
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
        api_token = "0ABCDEF0FF"
        cbpi.add_config_parameter("DynDns_API_token", "0ABCDEF0FF", "text", "Your API token")

    version = app.get_config_parameter("DynDns_IP_Version", None)
    if version is None:
        version = "4 & 6"
        cbpi.add_config_parameter("DynDns_IP_Version", "4 & 6", "select", "Do you want to update your IPv4 or IPv6?", ["4", "6", "4 & 6"])
        
