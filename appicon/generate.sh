#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o noclobber
set -o nounset
#set -o xtrace #debug

# Requirements:
#   magick                  (`brew install imagemagick`)
#   png2icns                (`brew install libicns`)

# Colors and formatting
NC=$'\033[0m'
BOLD=$'\033[1m'
DIM=$'\033[2m'
ITALIC=$'\033[3m'
ULINE=$'\033[4m'
RED=$'\033[1;31m'
GREEN=$'\033[1;32m'
YELLOW=$'\033[1;33m'
BLUE=$'\033[1;34m'
MAGENTA=$'\033[1;35m'
CYAN=$'\033[1;36m'
INFO="${BLUE}ℹ${NC}"
OK="${GREEN}✓${NC}"
WARN="${YELLOW}⚠${NC}"
ERROR="${RED}✖${NC}"

image_source=${1:-cambiomed-fish-icon.png}
image_target=${2:-preprocessor}
image_folder=${3:-.}

echo "${INFO} Source image: $image_source"
echo "${INFO} Icon prefix: $image_target"
echo "${INFO} Output folder: $image_folder"

#
hash magick   ||  { echo "${ERROR} Missing imagemagick/convert" ; exit 1 ; }
hash png2icns ||  { echo "${ERROR} Missing libicns/png2icns" ; exit 1 ; }
[ -f ${image_source} ] ||  { echo "${ERROR} Missing image_source: ${image_source}" ; exit 1 ; }

[ -d ${image_folder} ] || mkdir -p ${image_folder}

#
proper_spec_list=(
   "24x1" "48x1" "64x1" "96x1" "128x1"
   "20x1" "20x2" "20x3"
   "29x1" "29x2" "29x3"
   "40x1" "40x2" "40x3"
   "60x2" "60x3"
   "76x1" "76x2"
   "83.5x2" "1024x1"
)

convert_proper() {
    for image_spec in ${proper_spec_list[*]} ; do
       size=${image_spec%x*}
       scale=${image_spec##*x}
       resize=$(bc <<< ${size}*${scale} )
       echo "${INFO} apply ${image_source} spec: ${size}x${size}@${scale}"
       magick ${image_source} \
          -resize ${resize}x${resize} \
          -unsharp '1.5x1+0.7+0.02' \
          ${image_folder}/${image_target}-${size}x${size}@${scale}x.png
    done
}


android_spec_list=(
    48 72 96 144 192
)

convert_android() {
    convert_android_round
    convert_android_square
}

convert_android_round() {
    file_type="round"
    for image_spec in ${android_spec_list[*]} ; do
       size=${image_spec}
       scale=1
       resize=$(bc <<< ${size}*${scale} )
       corner=$(bc <<< ${size}*0.5 ) # 50%
       file_name="${image_target}-${file_type}-${size}.png"
       file_path="${image_folder}/${file_name}"
       mask_path="${image_folder}/round-mask.png"
       echo "${INFO} Android round ${size}x${size}@${scale}: $file_name"
       # produce mask
       magick -size ${resize}x${resize} xc:none \
          -draw "roundrectangle 0,0,${resize},${resize},${corner},${corner}" \
          ${mask_path}
       # produce resize
       magick ${image_source} \
          -resize ${resize}x${resize} \
          -unsharp '1.5x1+0.7+0.02' \
          ${file_path}
       # produce composite
       magick ${file_path} \
          -alpha Set ${mask_path} \
          -compose DstIn -composite \
          ${file_path}
       # destroy mask
       rm ${mask_path}
    done
}

convert_android_square() {
    file_type="square"
    for image_spec in ${android_spec_list[*]} ; do
       size=${image_spec}
       scale=1
       resize=$(bc <<< ${size}*${scale} )
       file_name="${image_target}-${file_type}-${size}.png"
       file_path="${image_folder}/${file_name}"
       echo "${INFO} Android square ${size}x${size}@${scale}: $file_name"
       magick ${image_source} \
          -resize ${resize}x${resize} \
          -unsharp '1.5x1+0.7+0.02' \
          ${file_path}
    done
}


ios_spec_list=(
    20 29 40 58 60 76 80 87 120 152 167 180 1024
)

convert_ios() {
    for image_spec in ${ios_spec_list[*]} ; do
       size=${image_spec}
       scale=1
       resize=$(bc <<< ${size}*${scale} )
       file_name="${image_target}-${size}.png"
       file_path="${image_folder}/${file_name}"
       echo "${INFO} iOS ${size}x${size}@${scale}: $file_name"
       magick ${image_source} \
          -resize ${resize}x${resize} \
          -unsharp '1.5x1+0.7+0.02' \
          ${file_path}
    done
}


macos_spec_list=(
    16 32 48 128 256 512
)

convert_macos() {
    file_list=""
    for image_spec in ${macos_spec_list[*]} ; do
       size=${image_spec}
       scale=1
       resize=$(bc <<< ${size}*${scale} )
       file_name="${image_target}-${size}.png"
       file_path="${image_folder}/${file_name}"
       echo "${INFO} macOS ${size}x${size}@${scale}: $file_name"
       magick ${image_source} \
          -resize ${resize}x${resize} \
          -unsharp '1.5x1+0.7+0.02' \
          ${file_path}
       file_list="${file_list} ${file_path}"
    done
    png2icns "${image_target}.icns" ${file_list[@]}
}


windows_spec_list="16,24,32,48,64,72,96,128,256"

convert_windows() {
    echo "${INFO} Windows ${windows_spec_list}"
    magick ${image_source} \
        -background transparent \
        -define icon:auto-resize=${windows_spec_list} \
        "${image_folder}/${image_target}.ico"
}

convert_default() {
    size="256"
    echo "${INFO} Default ${size}"
    src="${image_target}-256.png"
    dst="${image_target}.png"
    cp ${src} ${dst}
}


convert_android

convert_ios

convert_macos

convert_windows

convert_default