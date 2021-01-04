$csv = import-csv "C:\scripts\2021_LSR\2021_LSR.csv"
foreach($lsr in $CSV)
{
    $int = [int]$LSR.LSRNumber.split('-')[1]
    $req = Invoke-WebRequest -uri "http://www.gencourt.state.nh.us/lsr_search/billText.aspx?id=$($int)&type=4"
    if($req.Content -notmatch 'error'){$LSR.BillURL =  "http://www.gencourt.state.nh.us/lsr_search/billText.aspx?id=$($int)&type=4"}
}

$csv | export-csv "C:\scripts\2021_LSR\2021_LSR.csv" -NoTypeInformation