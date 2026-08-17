$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent $PSScriptRoot
$chapterDir = Get-ChildItem -LiteralPath $root -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName '_audit\rendered_pages')
} | Select-Object -First 1
if (-not $chapterDir) { throw 'Chapter directory not found.' }

$pages = Join-Path $chapterDir.FullName '_audit\rendered_pages'
$out = Join-Path $chapterDir.FullName 'images'
[System.IO.Directory]::CreateDirectory($out) | Out-Null

# name, page, left, top, width, height
$crops = @(
    @('ch16_logistic_function_derivative.png', 433, 180, 735, 1110, 445),
    @('ch16_threshold_comparison.png', 440, 180, 650, 850, 465),
    @('ch16_roc_curve.png', 442, 185, 555, 750, 580),
    @('ch17_knn_classification.png', 460, 185, 585, 1145, 595),
    @('ch17_knn_regression.png', 461, 185, 585, 730, 595),
    @('ch18_step_function.png', 478, 180, 715, 760, 460),
    @('ch18_tree_structure.png', 479, 180, 700, 965, 510),
    @('ch18_information_gain_example.png', 487, 175, 310, 1380, 790),
    @('ch18_pruning_depth.png', 488, 180, 535, 825, 650),
    @('ch18_classification_prediction.png', 491, 180, 370, 1310, 650),
    @('ch18_regression_prediction.png', 492, 180, 370, 1310, 810),
    @('ch19_spam_prediction.png', 515, 180, 740, 1730, 405)
)

foreach ($crop in $crops) {
    $name = [string]$crop[0]
    $page = [int]$crop[1]
    $source = Join-Path $pages ('page_{0:D3}.png' -f $page)
    $target = Join-Path $out $name
    $image = [System.Drawing.Image]::FromFile($source)
    try {
        $rect = [System.Drawing.Rectangle]::new(
            [int]$crop[2], [int]$crop[3], [int]$crop[4], [int]$crop[5]
        )
        $bitmap = [System.Drawing.Bitmap]::new($rect.Width, $rect.Height)
        try {
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            try {
                $graphics.DrawImage($image, 0, 0, $rect, [System.Drawing.GraphicsUnit]::Pixel)
            }
            finally { $graphics.Dispose() }
            $bitmap.Save($target, [System.Drawing.Imaging.ImageFormat]::Png)
        }
        finally { $bitmap.Dispose() }
    }
    finally { $image.Dispose() }
}
