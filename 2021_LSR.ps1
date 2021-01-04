mkdir C:\scripts -ErrorAction SilentlyContinue
mkdir C:\scripts\2021_LSR -ErrorAction SilentlyContinue
$list = New-Object System.Collections.Generic.List[object]
$req = Invoke-WebRequest -uri 'http://www.gencourt.state.nh.us/lsr_search/rss.aspx?cmbbody=&txttitle=&txtlsr=&comblast=' -OutFile C:\scripts\2021_LSR\2021_LSR.xml -PassThru
if($req.Content -eq 'Timeout expired.  The timeout period elapsed prior to completion of the operation or the server is not responding.'){write-host 'Server timed out, cannot continue';break}

[xml]$Content = Get-Content C:\scripts\2021_LSR\2021_LSR.xml
$Feed = $Content.rss.channel

foreach($LSR in $Feed.Item)
{
    $BillURL = ''
    $int = [int]$LSR.LSRNumber.split('-')[1]
    $req = Invoke-WebRequest -uri "http://www.gencourt.state.nh.us/lsr_search/billText.aspx?id=$($int)&type=4"
    if($req.Content -notmatch 'error'){$BillURL =  "http://www.gencourt.state.nh.us/lsr_search/billText.aspx?id=$($int)&type=4"}
    $obj = [PSCustomObject]@{
     'pubDate' = $LSR.pubDate
     'LSRNumber' = $LSR.LSRNumber
     'LSRTitle' = $LSR.LSRTitle
     'BillNumber' = $LSR.BillNumber
     'BillURL' = $BillURL
     'PrimeSponsor' = $LSR.Sponsors.PrimeSponsor
     }
     $list.add($obj)
}

$list | Export-Csv -Path 'C:\scripts\2021_LSR\2021_LSR.csv' -NoTypeInformation