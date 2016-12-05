$projectDir = "D:\Projects\coastalHeatCapacity"
Set-Location $projectDir

$hdfPath = "data\nasa\A20023552016080.L3m_SCWI_SST_sst_4km.nc"
$tmpDir = $env:temp
$outTiff = Join-Path -path $tmpDir -ChildPath "sst.tiff"
$clippedTiff = Join-Path -path $tmpDir -ChildPath "sstGB.tiff"

gdal_translate -ot Float32 -scale 0 65535 -2 45 -a_ullr -180 90 180 -90 -a_nodata 45 -a_srs EPSG:4326 HDF5:"$hdfPath"://sst $outTiff
gdalwarp -s_srs EPSG:4326 -t_srs EPSG:27700 -te 0 0 700000 1300000 $outTiff $clippedTiff
raster2pgsql -s 27700 $clippedTiff sst|psql -U postgres -d coastalheat

Remove-Item $outTiff
Remove-Item $clippedTiff
