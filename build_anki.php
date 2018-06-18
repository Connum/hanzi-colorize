<?php
$zip = new ZipArchive();
$filename = './dist/anki__hanzi_colorizer.zip';

$rootPath = './hanzicolorizer';

if (!is_dir('./dist')) {
	mkdir('./dist');
}

if (is_file($filename)) {
	unlink($filename);
}

if ($zip->open($filename, ZipArchive::CREATE)!==TRUE) {
    exit("cannot open <$filename>\n");
}

$files = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator($rootPath),
    RecursiveIteratorIterator::LEAVES_ONLY
);

$zip->addFile('anki/hanzi_colorizer.py', 'hanzi_colorizer.py');
foreach ($files as $name => $file)
{
    // Skip directories (they would be added automatically)
    if (
    	!$file->isDir()
    	&& (
    		(preg_match("@\.py$@", $file->getFileName()))
    		|| (preg_match("@\.svg$@", $file->getFileName()) && preg_match("@" . preg_quote("data" . DIRECTORY_SEPARATOR . "hanzivg" . DIRECTORY_SEPARATOR . "hanzi") . "$@", dirname($file->getPathName())))
    	)
    )
    {
        // Get real and relative path for current file
        $filePath = $file->getRealPath();
        $relativePath = preg_replace("@^" . preg_quote('./') . "@", "" , $file->getPathName());

        // Add current file to archive
        $zip->addFile($filePath, $relativePath);
    }
}

$zip->close();