import os
import argparse
import sys
from pathlib import Path

def should_exclude_directory(dir_path, exclude_dirs):
    """Проверяет, нужно ли исключить директорию"""
    dir_name = os.path.basename(dir_path)
    return dir_name in exclude_dirs

def should_exclude_file(file_path, exclude_files):
    """Проверяет, нужно ли исключить файл"""
    file_name = os.path.basename(file_path)
    return file_name in exclude_files

def is_text_file(file_path):
    """Проверяет, является ли файл текстовым"""
    text_extensions = {
        '.py'
    }

    file_ext = os.path.splitext(file_path)[1].lower()
    return file_ext in text_extensions

def read_file_content(file_path):
    """Читает содержимое файла с обработкой различных кодировок"""
    encodings = ['utf-8', 'cp1251', 'latin-1', 'ascii']

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            return f"[Ошибка чтения файла: {str(e)}]"

    return "[Не удалось прочитать файл - неподдерживаемая кодировка]"

def create_file_catalog(directory, output_file, exclude_dirs=None, exclude_files=None, include_binary=False):
    """Создает каталог файлов в указанной директории"""

    if exclude_dirs is None:
        exclude_dirs = set()
    else:
        exclude_dirs = set(exclude_dirs)

    # Добавляем стандартные директории для исключения
    default_excludes = {'.git', '__pycache__', '.vscode', '.idea', 'node_modules', '.env'}
    exclude_dirs.update(default_excludes)

    files_processed = 0

    try:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            out_f.write(f"# Каталог файлов директории: {os.path.abspath(directory)}\n")
            out_f.write(f"# Создано: {Path().cwd()}\n")
            out_f.write("# " + "="*60 + "\n\n")

            # Проходим по всем файлам в директории рекурсивно
            for root, dirs, files in os.walk(directory):
                # Исключаем директории из обхода
                dirs[:] = [d for d in dirs if not should_exclude_directory(os.path.join(root, d), exclude_dirs)]

                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory)

                    # Проверяем, является ли файл текстовым
                    if not include_binary and not is_text_file(file_path):
                        continue

                    try:
                        # Записываем заголовок файла
                        out_f.write(f"**{relative_path}**\n\n")

                        # Читаем и записываем содержимое
                        content = read_file_content(file_path)
                        out_f.write(content)
                        out_f.write("\n\n\n\n")

                        files_processed += 1
                        print(f"Обработан: {relative_path}")

                    except Exception as e:
                        print(f"Ошибка при обработке файла {relative_path}: {str(e)}")
                        continue

    except Exception as e:
        print(f"Ошибка при создании выходного файла: {str(e)}")
        return False

    print(f"\nГотово! Обработано файлов: {files_processed}")
    print(f"Результат сохранен в: {os.path.abspath(output_file)}")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Утилита для создания каталога файлов в директории",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python file_catalog.py /path/to/directory
  python file_catalog.py . -o catalog.txt
  python file_catalog.py /project -e tests docs build
  python file_catalog.py . -f package-lock.json yarn.lock
  python file_catalog.py . --include-binary -e .git node_modules -f .env config.json
        """
    )

    parser.add_argument(
        'directory',
        help='Путь к директории для обработки'
    )

    parser.add_argument(
        '-o', '--output',
        default='files_catalog.txt',
        help='Имя выходного файла (по умолчанию: files_catalog.txt)'
    )

    parser.add_argument(
        '-e', '--exclude',
        nargs='*',
        default=[],
        help='Список директорий для исключения'
    )

    parser.add_argument(
        '-f', '--exclude-files',
        nargs='*',
        default=[],
        help='Список файлов для исключения'
    )

    parser.add_argument(
        '--include-binary',
        action='store_true',
        help='Включать бинарные файлы (по умолчанию обрабатываются только текстовые)'
    )

    parser.add_argument(
        '--list-excluded',
        action='store_true',
        help='Показать список исключаемых директорий и файлов по умолчанию'
    )

    args = parser.parse_args()

    if args.list_excluded:
        default_excludes = {'.git', '__pycache__', '.vscode', '.idea', 'node_modules', '.env'}
        default_exclude_files = {'.gitignore', '.env', '.DS_Store', 'Thumbs.db'}
        print("Директории, исключаемые по умолчанию:")
        for exclude in sorted(default_excludes):
            print(f"  - {exclude}")
        print("\nФайлы, исключаемые по умолчанию:")
        for exclude in sorted(default_exclude_files):
            print(f"  - {exclude}")
        return

    # Проверяем существование директории
    if not os.path.isdir(args.directory):
        print(f"Ошибка: Директория '{args.directory}' не существует")
        sys.exit(1)

    print(f"Обработка директории: {os.path.abspath(args.directory)}")
    print(f"Выходной файл: {args.output}")

    if args.exclude:
        print(f"Исключаемые директории: {', '.join(args.exclude)}")

    if args.exclude_files:
        print(f"Исключаемые файлы: {', '.join(args.exclude_files)}")

    if args.include_binary:
        print("Режим: включая бинарные файлы")
    else:
        print("Режим: только текстовые файлы")

    # Создаем каталог файлов
    success = create_file_catalog(
        args.directory,
        args.output,
        args.exclude,
        args.exclude_files,
        args.include_binary
    )

    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()
