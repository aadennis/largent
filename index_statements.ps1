$months = @{
    Jan='01'; Feb='02'; Mar='03'; Apr='04'
    May='05'; Jun='06'; Jul='07'; Aug='08'
    Sep='09'; Oct='10'; Nov='11'; Dec='12'
}
$dir = "x" # replace with the actual directory path
Set-Location -Path $dir


Get-ChildItem *.pdf | ForEach-Object {
    $month = $_.Name.Split(' ')[0]
    Rename-Item $_ -NewName "$($months[$month]) $($_.Name)"
}
