---
description: 扫描并优化仓库中的所有图片（增强版）- 支持多种格式、批量处理、进度显示和详细报告
argument-hint: [format] [quality] [backup] [dry-run]
allowed-tools: Bash(find:*), Bash(which:*), Bash(file:*), Bash(mkdir:*), Bash(cp:*), Bash(mv:*), Bash(du:*), Bash(wc:*), Bash(stat:*)
---

# 优化图片（增强版）

我将帮助你扫描仓库中的所有图片文件并进行优化。这个增强版本提供了更详细的报告、进度显示和更好的错误处理。

## 步骤 1: 检查可用的优化工具

首先检查系统中可用的图片优化工具：

### 检查 ImageMagick

!`which magick convert 2>/dev/null | head -1 || echo "未找到 ImageMagick"`

### 检查 sharp-cli (Node.js)

!`which sharp-cli 2>/dev/null || echo "未找到 sharp-cli"`

### 检查 optipng

!`which optipng 2>/dev/null || echo "未找到 optipng"`

### 检查 jpegoptim

!`which jpegoptim 2>/dev/null || echo "未找到 jpegoptim"`

### 检查 cwebp (WebP)

!`which cwebp 2>/dev/null || echo "未找到 cwebp"`

### 检查 Python Pillow

!`python3 -c "from PIL import Image; print('Pillow 已安装')" 2>/dev/null || echo "未找到 Pillow"`

## 步骤 2: 扫描并分析图片文件

扫描仓库中的所有图片文件（排除 node_modules、.git 等目录）：

```bash
# 定义排除目录
EXCLUDE_DIRS="node_modules .git .next dist build .cache __pycache__ venv env .venv target out .idea .vscode"

# 构建排除模式
EXCLUDE_PATTERN=""
for dir in $EXCLUDE_DIRS; do
  EXCLUDE_PATTERN="$EXCLUDE_PATTERN ! -path \"*/$dir/*\""
done

# 查找所有图片文件
eval "find . -type f \( \
  -iname \"*.png\" -o \
  -iname \"*.jpg\" -o \
  -iname \"*.jpeg\" -o \
  -iname \"*.gif\" -o \
  -iname \"*.webp\" -o \
  -iname \"*.bmp\" -o \
  -iname \"*.tiff\" -o \
  -iname \"*.tif\" -o \
  -iname \"*.svg\" \
\) $EXCLUDE_PATTERN" | sort > /tmp/image_files.txt

# 显示找到的文件
cat /tmp/image_files.txt
```

### 统计图片文件

!`find . -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.gif" -o -iname "*.webp" -o -iname "*.bmp" -o -iname "*.tiff" -o -iname "*.tif" \) ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/.next/*" ! -path "*/dist/*" ! -path "*/build/*" ! -path "*/.cache/*" ! -path "*/__pycache__/*" ! -path "*/venv/*" ! -path "*/env/*" ! -path "*/.venv/*" ! -path "*/target/*" ! -path "*/out/*" 2>/dev/null | wc -l | tr -d ' '`

### 按类型分类统计

!`find . -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.gif" -o -iname "*.webp" -o -iname "*.bmp" -o -iname "*.tiff" -o -iname "*.tif" \) ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/.next/*" ! -path "*/dist/*" ! -path "*/build/*" ! -path "*/.cache/*" ! -path "*/__pycache__/*" ! -path "*/venv/*" ! -path "*/env/*" ! -path "*/.venv/*" ! -path "*/target/*" ! -path "*/out/*" 2>/dev/null -exec sh -c 'case "${1##*.}" in png|PNG) echo "PNG";; jpg|jpeg|JPG|JPEG) echo "JPEG";; gif|GIF) echo "GIF";; webp|WEBP) echo "WebP";; bmp|BMP) echo "BMP";; tiff|tif|TIFF|TIF) echo "TIFF";; esac' _ {} \; | sort | uniq -c | sort -rn`

### 计算总文件大小

!`find . -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.gif" -o -iname "*.webp" -o -iname "*.bmp" -o -iname "*.tiff" -o -iname "*.tif" \) ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/.next/*" ! -path "*/dist/*" ! -path "*/build/*" ! -path "*/.cache/*" ! -path "*/__pycache__/*" ! -path "*/venv/*" ! -path "*/env/*" ! -path "*/.venv/*" ! -path "*/target/*" ! -path "*/out/*" 2>/dev/null -exec du -ch {} + | tail -1 | cut -f1`

### 显示最大的图片文件（前10个）

!`find . -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.gif" -o -iname "*.webp" -o -iname "*.bmp" -o -iname "*.tiff" -o -iname "*.tif" \) ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/.next/*" ! -path "*/dist/*" ! -path "*/build/*" ! -path "*/.cache/*" ! -path "*/__pycache__/*" ! -path "*/venv/*" ! -path "*/env/*" ! -path "*/.venv/*" ! -path "*/target/*" ! -path "*/out/*" 2>/dev/null -exec du -h {} + | sort -rh | head -10`

## 步骤 3: 创建备份（如果指定）

如果指定了 `backup` 参数，创建备份目录：

```bash
BACKUP_DIR=".image-backup-$(date +%Y%m%d-%H%M%S)"
DRY_RUN=${4:-""}

if [ "$3" = "backup" ] || [ -n "$3" ]; then
  if [ "$DRY_RUN" != "dry-run" ]; then
    echo "创建备份目录: $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"

    # 备份所有图片文件
    find . -type f \( \
      -iname "*.png" -o \
      -iname "*.jpg" -o \
      -iname "*.jpeg" -o \
      -iname "*.gif" -o \
      -iname "*.webp" -o \
      -iname "*.bmp" -o \
      -iname "*.tiff" -o \
      -iname "*.tif" \
    \) ! -path "*/node_modules/*" \
      ! -path "*/.git/*" \
      ! -path "*/.next/*" \
      ! -path "*/dist/*" \
      ! -path "*/build/*" \
      ! -path "*/.cache/*" \
      ! -path "*/__pycache__/*" \
      ! -path "*/venv/*" \
      ! -path "*/env/*" \
      ! -path "*/.venv/*" \
      ! -path "*/target/*" \
      ! -path "*/out/*" \
      -exec sh -c 'mkdir -p "$1/$(dirname "$2")" && cp "$2" "$1/$2"' _ "$BACKUP_DIR" {} \;

    echo "备份完成: $BACKUP_DIR"
    echo "备份文件数: $(find "$BACKUP_DIR" -type f | wc -l | tr -d ' ')"
    echo "备份大小: $(du -sh "$BACKUP_DIR" | cut -f1)"
  else
    echo "[DRY RUN] 将创建备份目录: $BACKUP_DIR"
  fi
fi
```

## 步骤 4: 优化图片（智能选择工具）

根据可用的工具和文件类型智能选择优化方法：

```bash
#!/bin/bash

# 参数设置
FORMAT=${1:-"keep"}
QUALITY=${2:-85}
BACKUP_FLAG=${3:-""}
DRY_RUN=${4:-""}

# 排除目录
EXCLUDE_DIRS="node_modules .git .next dist build .cache __pycache__ venv env .venv target out .idea .vscode"
EXCLUDE_PATTERN=""
for dir in $EXCLUDE_DIRS; do
  EXCLUDE_PATTERN="$EXCLUDE_PATTERN ! -path \"*/$dir/*\""
done

# 统计变量
TOTAL_FILES=0
OPTIMIZED_FILES=0
FAILED_FILES=0
TOTAL_SAVED=0

# 优化函数
optimize_image() {
  local file="$1"
  local format="$2"
  local quality="$3"
  local dry_run="$4"
  
  local ext="${file##*.}"
  local name="${file%.*}"
  local original_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
  
  if [ "$dry_run" = "dry-run" ]; then
    echo "[DRY RUN] 将优化: $file (${original_size} bytes)"
    return 0
  fi
  
  # 根据文件类型和可用工具选择优化方法
  case "$ext" in
    png|PNG)
      if command -v optipng &> /dev/null; then
        optipng -o2 -quiet "$file" && {
          local new_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
          local saved=$((original_size - new_size))
          echo "✓ PNG 优化: $file (节省: $(numfmt --to=iec-i --suffix=B $saved 2>/dev/null || echo "${saved}B"))"
          return 0
        }
      elif command -v magick &> /dev/null || command -v convert &> /dev/null; then
        local convert_cmd=$(which magick 2>/dev/null || which convert 2>/dev/null)
        $convert_cmd "$file" -strip -quality 90 "$file" && {
          echo "✓ PNG 优化 (ImageMagick): $file"
          return 0
        }
      fi
      ;;
    jpg|jpeg|JPG|JPEG)
      if command -v jpegoptim &> /dev/null; then
        jpegoptim --max="$quality" --strip-all --preserve --quiet "$file" && {
          local new_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
          local saved=$((original_size - new_size))
          echo "✓ JPEG 优化: $file (节省: $(numfmt --to=iec-i --suffix=B $saved 2>/dev/null || echo "${saved}B"))"
          return 0
        }
      elif command -v magick &> /dev/null || command -v convert &> /dev/null; then
        local convert_cmd=$(which magick 2>/dev/null || which convert 2>/dev/null)
        $convert_cmd "$file" -strip -quality "$quality" "$file" && {
          echo "✓ JPEG 优化 (ImageMagick): $file"
          return 0
        }
      fi
      ;;
    webp|WEBP)
      # WebP 文件通常已经优化过，跳过
      echo "⊘ WebP 跳过: $file (已优化格式)"
      return 0
      ;;
    gif|GIF)
      if command -v magick &> /dev/null || command -v convert &> /dev/null; then
        local convert_cmd=$(which magick 2>/dev/null || which convert 2>/dev/null)
        $convert_cmd "$file" -strip "$file" && {
          echo "✓ GIF 优化: $file"
          return 0
        }
      fi
      ;;
  esac
  
  # 格式转换
  if [ "$format" != "keep" ] && [ "$format" != "$ext" ]; then
    if [ "$format" = "webp" ] && command -v cwebp &> /dev/null; then
      cwebp -q "$quality" "$file" -o "$name.webp" && {
        local new_size=$(stat -f%z "$name.webp" 2>/dev/null || stat -c%s "$name.webp" 2>/dev/null || echo 0)
        local saved=$((original_size - new_size))
        echo "✓ 转换为 WebP: $file -> $name.webp (节省: $(numfmt --to=iec-i --suffix=B $saved 2>/dev/null || echo "${saved}B"))"
        return 0
      }
    elif command -v magick &> /dev/null || command -v convert &> /dev/null; then
      local convert_cmd=$(which magick 2>/dev/null || which convert 2>/dev/null)
      if [ "$format" = "webp" ]; then
        $convert_cmd "$file" -quality "$quality" "$name.webp" && {
          echo "✓ 转换为 WebP (ImageMagick): $file -> $name.webp"
          return 0
        }
      fi
    fi
  fi
  
  echo "✗ 无法优化: $file (无可用工具或格式不支持)"
  return 1
}

# 主处理循环
echo "开始优化图片..."
echo "格式: $FORMAT"
echo "质量: $QUALITY%"
echo "模式: ${DRY_RUN:-实际执行}"
echo ""

eval "find . -type f \( \
  -iname \"*.png\" -o \
  -iname \"*.jpg\" -o \
  -iname \"*.jpeg\" -o \
  -iname \"*.gif\" -o \
  -iname \"*.webp\" \
\) $EXCLUDE_PATTERN" | while read -r file; do
  TOTAL_FILES=$((TOTAL_FILES + 1))
  if optimize_image "$file" "$FORMAT" "$QUALITY" "$DRY_RUN"; then
    OPTIMIZED_FILES=$((OPTIMIZED_FILES + 1))
  else
    FAILED_FILES=$((FAILED_FILES + 1))
  fi
  
  # 显示进度
  if [ $((TOTAL_FILES % 10)) -eq 0 ]; then
    echo "进度: $TOTAL_FILES 个文件已处理..."
  fi
done

echo ""
echo "=== 优化完成 ==="
echo "总文件数: $TOTAL_FILES"
echo "成功优化: $OPTIMIZED_FILES"
echo "失败/跳过: $FAILED_FILES"
```

## 步骤 5: 使用 Python 进行高级优化（如果可用）

如果安装了 Python Pillow，可以使用更高级的优化功能：

```bash
if command -v python3 &> /dev/null; then
  python3 << 'PYTHON_SCRIPT'
import os
import sys
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image, ImageOps
except ImportError:
    print("未安装 Pillow，跳过 Python 优化")
    sys.exit(0)

def get_file_size(file_path):
    """获取文件大小（字节）"""
    return os.path.getsize(file_path)

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def optimize_image_advanced(file_path, quality=85, format_override=None, dry_run=False):
    """高级图片优化"""
    try:
        original_size = get_file_size(file_path)
        ext = Path(file_path).suffix.lower()
        
        # 跳过 SVG（矢量图）
        if ext == '.svg':
            return {'status': 'skipped', 'reason': 'SVG format'}
        
        with Image.open(file_path) as img:
            # 获取图片信息
            width, height = img.size
            mode = img.mode
            
            # 转换为 RGB（如果需要）
            if img.mode in ('RGBA', 'LA', 'P'):
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[3])
                img = background
            
            # 确定输出格式和路径
            if format_override:
                output_format = format_override.upper()
                output_path = str(Path(file_path).with_suffix(f'.{format_override}'))
            else:
                output_format = 'JPEG' if ext in ['.jpg', '.jpeg'] else 'PNG'
                output_path = file_path
            
            if dry_run:
                return {
                    'status': 'dry_run',
                    'original_size': original_size,
                    'file': file_path
                }
            
            # 保存优化后的图片
            if output_format == 'JPEG':
                img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            elif output_format == 'PNG':
                img.save(output_path, 'PNG', optimize=True, compress_level=9)
            elif output_format == 'WEBP':
                img.save(output_path, 'WEBP', quality=quality, method=6)
            else:
                img.save(output_path, output_format, optimize=True)
            
            new_size = get_file_size(output_path)
            saved = original_size - new_size
            saved_percent = (saved / original_size * 100) if original_size > 0 else 0
            
            return {
                'status': 'success',
                'original_size': original_size,
                'new_size': new_size,
                'saved': saved,
                'saved_percent': saved_percent,
                'file': file_path,
                'output': output_path if format_override else file_path
            }
    except Exception as e:
        return {'status': 'error', 'error': str(e), 'file': file_path}

# 扫描图片文件
exclude_dirs = {
    'node_modules', '.git', '.next', 'dist', 'build', '.cache', 
    '__pycache__', 'venv', 'env', '.venv', 'target', 'out', 
    '.idea', '.vscode', '.image-backup-*'
}

image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.tiff', '.tif'}

# 解析参数
quality = int(sys.argv[1]) if len(sys.argv) > 1 else 85
format_override = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != 'keep' else None
dry_run = len(sys.argv) > 3 and sys.argv[3] == 'dry-run'

results = {
    'total': 0,
    'success': 0,
    'skipped': 0,
    'error': 0,
    'total_original_size': 0,
    'total_new_size': 0,
    'total_saved': 0
}

print(f"开始优化图片...")
print(f"质量: {quality}%")
print(f"格式: {format_override or '保持原格式'}")
print(f"模式: {'DRY RUN' if dry_run else '实际执行'}")
print("")

for root, dirs, files in os.walk('.'):
    # 排除目录
    dirs[:] = [d for d in dirs if not any(d.startswith(exclude.replace('*', '')) for exclude in exclude_dirs)]
    
    for file in files:
        file_path = Path(root) / file
        if file_path.suffix.lower() in image_extensions:
            results['total'] += 1
            result = optimize_image_advanced(str(file_path), quality, format_override, dry_run)
            
            if result['status'] == 'success':
                results['success'] += 1
                results['total_original_size'] += result['original_size']
                results['total_new_size'] += result['new_size']
                results['total_saved'] += result['saved']
                print(f"✓ {file_path}: {format_size(result['original_size'])} -> {format_size(result['new_size'])} "
                      f"(节省 {result['saved_percent']:.1f}%)")
            elif result['status'] == 'dry_run':
                results['total_original_size'] += result['original_size']
                print(f"[DRY RUN] {file_path}: {format_size(result['original_size'])}")
            elif result['status'] == 'skipped':
                results['skipped'] += 1
                print(f"⊘ 跳过 {file_path}: {result.get('reason', '')}")
            else:
                results['error'] += 1
                print(f"✗ 错误 {file_path}: {result.get('error', 'Unknown error')}")

print("")
print("=== 优化统计 ===")
print(f"总文件数: {results['total']}")
print(f"成功优化: {results['success']}")
print(f"跳过: {results['skipped']}")
print(f"错误: {results['error']}")
if results['success'] > 0:
    print(f"原始总大小: {format_size(results['total_original_size'])}")
    print(f"优化后大小: {format_size(results['total_new_size'])}")
    print(f"总共节省: {format_size(results['total_saved'])} "
          f"({results['total_saved'] / results['total_original_size'] * 100:.1f}%)")
PYTHON_SCRIPT
fi
```

## 步骤 6: 生成优化报告

优化完成后，生成详细的报告：

```bash
echo ""
echo "=== 优化报告 ==="
echo "生成时间: $(date)"
echo ""

# 统计优化后的文件
echo "图片文件统计:"
find . -type f \( \
  -iname "*.png" -o \
  -iname "*.jpg" -o \
  -iname "*.jpeg" -o \
  -iname "*.gif" -o \
  -iname "*.webp" \
\) ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  ! -path "*/.next/*" \
  ! -path "*/dist/*" \
  ! -path "*/build/*" \
  ! -path "*/.cache/*" \
  ! -path "*/__pycache__/*" \
  ! -path "*/venv/*" \
  ! -path "*/env/*" \
  ! -path "*/.venv/*" \
  ! -path "*/target/*" \
  ! -path "*/out/*" \
  -exec sh -c 'echo "$(du -h "$1" | cut -f1) - $1"' _ {} \; | sort -h | head -20

echo ""
echo "=== 文件大小分布 ==="
find . -type f \( \
  -iname "*.png" -o \
  -iname "*.jpg" -o \
  -iname "*.jpeg" -o \
  -iname "*.gif" -o \
  -iname "*.webp" \
\) ! -path "*/node_modules/*" \
  ! -path "*/.git/*" \
  ! -path "*/.next/*" \
  ! -path "*/dist/*" \
  ! -path "*/build/*" \
  ! -path "*/.cache/*" \
  ! -path "*/__pycache__/*" \
  ! -path "*/venv/*" \
  ! -path "*/env/*" \
  ! -path "*/.venv/*" \
  ! -path "*/target/*" \
  ! -path "*/out/*" \
  -exec sh -c '
    size=$(stat -f%z "$1" 2>/dev/null || stat -c%s "$1" 2>/dev/null || echo 0)
    if [ $size -lt 102400 ]; then
      echo "小 (<100KB): $1"
    elif [ $size -lt 1048576 ]; then
      echo "中 (100KB-1MB): $1"
    else
      echo "大 (>1MB): $1"
    fi
  ' _ {} \; | sort
```

**使用方法：**

- `/optimize-images-enhanced` - 扫描并优化所有图片（保持原格式）
- `/optimize-images-enhanced webp` - 将所有图片转换为 WebP 格式
- `/optimize-images-enhanced keep 90` - 优化图片，质量设置为 90%
- `/optimize-images-enhanced webp 85 backup` - 转换为 WebP，质量 85%，并创建备份
- `/optimize-images-enhanced keep 85 backup dry-run` - 预览模式，不实际执行优化

**参数说明：**

- `format` (第一个参数):
  - `keep` 或留空 - 保持原格式
  - `webp` - 转换为 WebP 格式
  - 其他格式名称 - 转换为指定格式

- `quality` (第二个参数):
  - 数字 1-100，默认 85
  - 仅对 JPEG 和 WebP 有效

- `backup` (第三个参数):
  - 如果提供，会在优化前创建备份

- `dry-run` (第四个参数):
  - 如果提供，只显示将要执行的操作，不实际修改文件

**增强功能：**

1. ✅ 详细的文件统计和大小分析
2. ✅ 进度显示和错误处理
3. ✅ 多种优化工具自动选择
4. ✅ 文件大小节省统计
5. ✅ 支持预览模式（dry-run）
6. ✅ 更完善的排除目录列表
7. ✅ 优化报告生成

**推荐工具安装：**

- **macOS**: `brew install imagemagick optipng jpegoptim webp`
- **Ubuntu/Debian**: `sudo apt-get install imagemagick optipng jpegoptim webp`
- **Python Pillow**: `pip install Pillow`

**注意事项：**

- 优化会直接修改原文件（除非转换为新格式）
- 建议先使用 `dry-run` 预览将要执行的操作
- 建议使用 `backup` 参数创建备份
- 某些工具可能需要单独安装
- SVG 文件不会被优化（矢量图不需要优化）
- 大文件优化可能需要较长时间
