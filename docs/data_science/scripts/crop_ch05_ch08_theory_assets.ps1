$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent $PSScriptRoot
$chapterDir = Get-ChildItem -LiteralPath $root -Directory | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName '05_*.md')
} | Select-Object -First 1
if (-not $chapterDir) {
    $chapterDir = Get-ChildItem -LiteralPath $root -Directory | Where-Object {
        Test-Path -LiteralPath (Join-Path $_.FullName '_audit\rendered_pages')
    } | Select-Object -First 1
}
if (-not $chapterDir) { throw 'Chapter directory not found.' }
$pages = Join-Path $chapterDir.FullName '_audit\rendered_pages'
$out = Join-Path $chapterDir.FullName 'images'
[System.IO.Directory]::CreateDirectory($out) | Out-Null

$crops = @(
    @('ch05_total_probability_partition.png', 139, 170, 690, 705, 410),
    @('ch06_pdf_cdf.png', 161, 900, 630, 610, 405),
    @('bernoulli_shapes.png', 164, 170, 285, 1275, 480),
    @('ch06_binomial_distribution.png', 166, 170, 620, 780, 545),
    @('ch07_uniform_distribution.png', 183, 170, 555, 775, 555),
    @('ch07_normal_critical_regions.png', 185, 170, 690, 760, 500),
    @('ch07_t_distribution_family.png', 187, 170, 620, 695, 550),
    @('ch07_exponential_family.png', 189, 170, 690, 680, 470),
    @('ch07_gamma_family.png', 191, 170, 690, 680, 470),
    @('chi_square_family.png', 193, 170, 620, 760, 545),
    @('clt_sample_means.png', 211, 175, 380, 1025, 655),
    @('ch08_sampling_distribution.png', 213, 1080, 435, 740, 550)
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
            finally {
                $graphics.Dispose()
            }
            $bitmap.Save($target, [System.Drawing.Imaging.ImageFormat]::Png)
        }
        finally {
            $bitmap.Dispose()
        }
    }
    finally {
        $image.Dispose()
    }
}
