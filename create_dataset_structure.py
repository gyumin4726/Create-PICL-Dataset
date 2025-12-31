import os
import shutil
from pathlib import Path

def create_dataset_structure(source_dir, dataset_dir):
    """
    DATASET 폴더 안에 train/test 구조를 생성하고 이미지를 복사합니다.
    JSON 파일은 복사하지 않습니다.
    """
    
    # DATASET 폴더 생성
    dataset_path = Path(dataset_dir)
    train_path = dataset_path / "train"
    test_path = dataset_path / "test"
    
    train_path.mkdir(parents=True, exist_ok=True)
    test_path.mkdir(parents=True, exist_ok=True)
    
    # 조직 목록
    tissues = [
        'epidermis', 'dermis', 'subcutaneous_fat', 'muscle', 'cortical_bone',
        'csf', 'gray_matter', 'white_matter', 'whole_blood', 'tumor'
    ]
    
    # 각 조직별로 처리
    for tissue in tissues:
        source_tissue_dir = Path(source_dir) / tissue
        
        if not source_tissue_dir.exists():
            print(f"Warning: {source_tissue_dir} not found, skipping...")
            continue
        
        print(f"\nProcessing {tissue}...")
        
        # 샘플 폴더 목록 가져오기
        sample_folders = sorted([f for f in os.listdir(source_tissue_dir) 
                               if (source_tissue_dir / f).is_dir()])
        
        if len(sample_folders) != 300:
            raise ValueError(f"ERROR: {tissue} has {len(sample_folders)} samples, expected 300")
        
        # Train 샘플 (001-200)
        train_sample_folders = sample_folders[:200]
        train_tissue_dir = train_path / tissue
        train_tissue_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"  Copying train samples (001-200)...")
        train_count = 0
        for sample_folder in train_sample_folders:
            source_sample = source_tissue_dir / sample_folder
            dest_sample = train_tissue_dir / sample_folder
            
            # 샘플 폴더 복사
            if dest_sample.exists():
                shutil.rmtree(dest_sample)
            shutil.copytree(source_sample, dest_sample)
            train_count += 1
        
        print(f"    Copied {train_count} train samples")
        
        # Test 샘플 (201-300)
        test_sample_folders = sample_folders[200:]
        test_tissue_dir = test_path / tissue
        test_tissue_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"  Copying test samples (201-300)...")
        test_count = 0
        for sample_folder in test_sample_folders:
            source_sample = source_tissue_dir / sample_folder
            dest_sample = test_tissue_dir / sample_folder
            
            # 샘플 폴더 복사
            if dest_sample.exists():
                shutil.rmtree(dest_sample)
            shutil.copytree(source_sample, dest_sample)
            test_count += 1
        
        print(f"    Copied {test_count} test samples")
    
    print(f"\n{'=' * 50}")
    print(f"완료!")
    print(f"  - Train: {train_path}")
    print(f"  - Test: {test_path}")
    print(f"  - JSON 파일은 수동으로 옮겨주세요")
    print(f"{'=' * 50}")

if __name__ == "__main__":
    # 원본 데이터가 있는 디렉토리 (DATASET 폴더 안에 조직 폴더들이 있음)
    source_dir = r"C:\Users\user\Downloads\create data\DATASET"
    
    # DATASET 폴더 경로 (출력 경로)
    dataset_dir = r"C:\Users\user\Downloads\create data\DATASET"
    
    print("=" * 50)
    print("DATASET 폴더 구조 생성 중...")
    print("(이미지 파일만 복사, JSON 파일은 제외)")
    print("=" * 50)
    create_dataset_structure(source_dir, dataset_dir)

