show_same_page ()
{
    echo "Content-type: text/html"
    echo ""
    echo '<html>'
    echo '<head>'
    echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
    echo '<title>Miner</title>'
    echo '</head>'
    echo '<SCRIPT LANGUAGE="JavaScript">'
    echo 'window.location = "'$HTTP_REFERER'";'
    echo '</SCRIPT>'
    echo '<body>'
    echo '</body>'
    echo '</html>' 
}

show_apply_changes ()
{
    echo '<!DOCTYPE html>'
    echo '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" lang="en-US">'
    echo '<head>'
    echo '    <title>Miner</title>'
    echo '    <meta charset="UTF-8" />'
    echo '    <link href="../style.css" rel="stylesheet" type="text/css">'
    echo '    <link href="../grid.css" rel="stylesheet" type="text/css">'
    echo '    <link href="../type/type.css" rel="stylesheet" type="text/css">'

    echo '    <SCRIPT LANGUAGE="JavaScript">'
    echo '        function delayer(){'
    echo '            window.location = "'$HTTP_REFERER'";'
    echo '        }'
    echo '    </SCRIPT>'

    echo '</head>'

    echo '<body>'
    echo -n '<body onLoad="setTimeout('
    echo -n "'delayer()'"
    echo ', 1000)">'
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
    echo '                    <h1>Updating Configuration!!</h1>'
    echo '                </div>'
    echo '            </div>'
    echo '        </div>'
    echo '    </div>'
    echo '</div>'
    
    echo '</body>'
    echo '</html>' 
}

show_msg ()
{
    echo '<!DOCTYPE html>'
    echo '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" lang="en-US">'
    echo '<head>'
    echo '    <title>Miner</title>'
    echo '    <meta charset="UTF-8" />'
    echo '    <link href="../style.css" rel="stylesheet" type="text/css">'
    echo '    <link href="../grid.css" rel="stylesheet" type="text/css">'
    echo '    <link href="../type/type.css" rel="stylesheet" type="text/css">'

    echo '    <SCRIPT LANGUAGE="JavaScript">'
    echo '        function delayer(){'
    if [ "$2" = "" ] ; then
       echo '            window.location = "'$HTTP_REFERER'";'
    else
        echo '            window.location = "http://'$SERVER_NAME'/'$2'";'
    fi
    echo '        }'
    echo '    </SCRIPT>'

    echo '</head>'

    echo '<body>'
    echo -n '<body onLoad="setTimeout('
    echo -n "'delayer()'"
    echo ', 1000)">'
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
    echo $1
    echo '                   </h1>'
    echo '                </div>'
    echo '            </div>'
    echo '        </div>'
    echo '    </div>'
    echo '</div>'
    
    echo '</body>'
    echo '</html>' 
}
