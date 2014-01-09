# $1 == msg to show
# $2 == place to return to (optional)
# $3 == time to delay (optional)

show_msg ()
{
    msg=$1
    if [ "$2" = "" ] ; then
	return_page="$HTTP_REFERER"
    else
	return_page="http://$SERVER_NAME$2"
    fi
    if [ "$3" = "" ] ; then
	delay_time=1000
    else
	delay_time=$3
    fi
    
    echo '<!DOCTYPE html>'
    echo '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" lang="en-US">'
    echo '<head>'
    echo '    <title>Miner</title>'
    echo '    <meta charset="UTF-8" />'
    echo '    <link href="/style.css" rel="stylesheet" type="text/css">'
    echo '    <link href="/grid.css" rel="stylesheet" type="text/css">'
    echo '    <link href="/type/type.css" rel="stylesheet" type="text/css">'

    echo '    <SCRIPT LANGUAGE="JavaScript">'
    echo '        function delayer(){'
    echo '            window.location = "'$return_page'";'
    echo '        }'
    echo '    </SCRIPT>'

    echo '</head>'

    echo '<body>'
    echo -n '<body onLoad="setTimeout('
    echo -n "'delayer()'"
    echo -n ', '
    echo -n $delay_time
    echo ')">'

    echo '<div id="wrapper">'
    echo '    <header>'
    echo '        <div id="logo" class="col span_6_of_12">'
    echo '            <img src="../images/logo.png" alt="KnCMiner logo">'
    echo '        </div>'
    echo '    </header>'
    echo '    <div id="header" class="section">'
    echo '        <div class="span_12_of_12">'
    echo '            <div class="xbox box">'
    echo '                <div class="span_7_of_12">'
    echo '                    <h1>'
    echo $msg
    echo '                   </h1>'
    echo '                </div>'
    echo '            </div>'
    echo '        </div>'
    echo '    </div>'
    echo '</div>'
    
    echo '</body>'
    echo '</html>' 
}

urldecode () {
    tmp="`echo "${1}" | sed -e 's/+/ /g'`"
    printf  '%b' "${tmp//%/\\x}" 
}
