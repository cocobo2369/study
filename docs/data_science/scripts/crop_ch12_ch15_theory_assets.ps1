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
    @('ch12_confusion_matrix.png', 333, 175, 500, 1145, 705),
    @('ch13_underfit_optimal_overfit.png', 347, 170, 455, 1480, 525),
    @('ch13_bias_variance_tradeoff.png', 348, 175, 550, 800, 470),
    @('ch13_cosine_directions.png', 358, 175, 550, 980, 365),
    @('ch13_normalization_leakage_table.png', 360, 580, 550, 790, 520),
    @('ch14_error_residual.png', 377, 170, 470, 835, 555),
    @('ch14_ols_residuals.png', 378, 170, 520, 835, 560),
    @('ch14_qq_plots.png', 388, 175, 610, 1395, 490),
    @('ch15_regression_output.png', 403, 175, 540, 1150, 330),
    @('ch15_vif_before_after.png', 410, 175, 625, 1260, 400),
    @('ch15_residual_patterns.png', 416, 175, 390, 1470, 690)
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
