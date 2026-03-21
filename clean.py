import re
import os

def remove_punctuation(text):
    """
    Remove periods, commas, question marks, and exclamation points from text
    """
    # Remove specified punctuation
    punctuation = r'[.,?!]'
    text = re.sub(punctuation, '', text)
    
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def clean_train_list(input_file):
    """
    Read train.list, clean punctuation from the text after EN|, and save back
    """
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        return False
    
    cleaned_lines = []
    modified_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            original_line = line.rstrip('\n')
            
            # Skip empty lines
            if not original_line:
                cleaned_lines.append(original_line)
                continue
            
            # Split by pipe character
            parts = original_line.split('|')
            
            # Check if we have at least 4 parts (audio, train, lang, text)
            if len(parts) >= 4:
                # The text is the 4th part (index 3)
                original_text = parts[3]
                cleaned_text = remove_punctuation(original_text)
                
                # Only count as modified if punctuation was actually removed
                if original_text != cleaned_text:
                    modified_count += 1
                    print(f"Line {line_num}:")
                    print(f"  Original: {original_text[:100]}{'...' if len(original_text) > 100 else ''}")
                    print(f"  Cleaned:  {cleaned_text[:100]}{'...' if len(cleaned_text) > 100 else ''}")
                    print()
                
                # Replace the text part with cleaned version
                parts[3] = cleaned_text
                cleaned_line = '|'.join(parts)
                cleaned_lines.append(cleaned_line)
            else:
                # If line doesn't have expected format, keep as is
                print(f"Warning: Line {line_num} has unexpected format, keeping unchanged")
                cleaned_lines.append(original_line)
    
    # Write back to the same file
    with open(input_file, 'w', encoding='utf-8') as f:
        for line in cleaned_lines:
            f.write(line + '\n')
    
    print(f"\nCompleted processing {input_file}")
    print(f"Modified {modified_count} lines")
    
    return True

def main():
    # Path to train.list file
    train_list_path = "train.list"
    
    print(f"Cleaning punctuation from {train_list_path}...")
    print("=" * 60)
    
    # Clean the file
    success = clean_train_list(train_list_path)
    
    if success:
        print("\n" + "=" * 60)
        print("File cleaned successfully!")
        print(f"All periods (.), commas (,), question marks (?), and exclamation points (!) have been removed")
        print("from the text after 'EN|' in each line.")
    else:
        print("Failed to clean the file. Please check if train.list exists.")

if __name__ == "__main__":
    main()
