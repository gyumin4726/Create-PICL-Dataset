import os
import json

def generate_dataset_labels(root_dir, split='train'):
    """
    데이터셋 라벨 정보를 JSON 파일로 생성합니다.
    split: 'train' 또는 'test'
    """
    
    # 조직별 광학 특성 정의 (ID, μₐ, μₛ, g, n)
    tissue_properties = {
        'epidermis': {
            'tissue_id': 0,
            'mu_a': 0.03,
            'mu_s': 10.0,
            'g': 0.90,
            'n': 1.40,
            'name_kr': '표피'
        },
        'dermis': {
            'tissue_id': 1,
            'mu_a': 0.02,
            'mu_s': 20.0,
            'g': 0.90,
            'n': 1.40,
            'name_kr': '진피'
        },
        'subcutaneous_fat': {
            'tissue_id': 2,
            'mu_a': 0.01,
            'mu_s': 10.0,
            'g': 0.89,
            'n': 1.44,
            'name_kr': '지방 조직'
        },
        'muscle': {
            'tissue_id': 3,
            'mu_a': 0.02,
            'mu_s': 15.0,
            'g': 0.92,
            'n': 1.37,
            'name_kr': '골격근'
        },
        'cortical_bone': {
            'tissue_id': 4,
            'mu_a': 0.015,
            'mu_s': 20.0,
            'g': 0.90,
            'n': 1.50,
            'name_kr': '피질골'
        },
        'csf': {
            'tissue_id': 5,
            'mu_a': 0.0005,
            'mu_s': 0.005,
            'g': 0.90,
            'n': 1.33,
            'name_kr': '뇌척수액'
        },
        'gray_matter': {
            'tissue_id': 6,
            'mu_a': 0.02,
            'mu_s': 12.0,
            'g': 0.90,
            'n': 1.37,
            'name_kr': '뇌 회색질'
        },
        'white_matter': {
            'tissue_id': 7,
            'mu_a': 0.015,
            'mu_s': 25.0,
            'g': 0.95,
            'n': 1.38,
            'name_kr': '뇌 백질'
        },
        'whole_blood': {
            'tissue_id': 8,
            'mu_a': 0.50,
            'mu_s': 50.0,
            'g': 0.95,
            'n': 1.37,
            'name_kr': '전혈'
        },
        'tumor': {
            'tissue_id': 9,
            'mu_a': 0.03,
            'mu_s': 20.0,
            'g': 0.92,
            'n': 1.38,
            'name_kr': '종양 조직'
        }
    }
    
    # split에 따라 설정
    if split == 'train':
        start_idx = 0
        end_idx = 200
        expected_count = 200
        dataset_name = 'Temporal_Dynamics_Optical_Dataset_Train'
        description = 'Train set: Time-gated optical scattering images for tissue optical properties estimation'
    elif split == 'test':
        start_idx = 200
        end_idx = 300
        expected_count = 100
        dataset_name = 'Temporal_Dynamics_Optical_Dataset_Test'
        description = 'Test set: Time-gated optical scattering images for tissue optical properties estimation'
    else:
        raise ValueError(f"Invalid split: {split}. Must be 'train' or 'test'")
    
    # 데이터셋 정보 초기화
    dataset_info = {
        'dataset_name': dataset_name,
        'description': description,
        'split': split,
        'total_samples': 0,
        'tissues': list(tissue_properties.keys()),
        'tissue_properties': tissue_properties,
        'time_gates': {
            'gate_0': '0-1 ns',
            'gate_1': '1-2 ns', 
            'gate_2': '2-3 ns',
            'gate_3': '3-4 ns',
            'gate_4': '4-5 ns'
        },
        'samples': []
    }
    
    # 각 조직별로 샘플 수집
    for tissue in tissue_properties.keys():
        tissue_dir = os.path.join(root_dir, tissue)
        
        # 조직 폴더가 없으면 오류 발생
        if not os.path.exists(tissue_dir):
            raise FileNotFoundError(f"ERROR: Tissue directory not found: {tissue_dir}")
        
        if not os.path.isdir(tissue_dir):
            raise ValueError(f"ERROR: {tissue_dir} is not a directory")
        
        print(f"Processing {tissue} ({split})...")
        
        # 각 샘플 폴더 확인 (예: cortical_bone001, cortical_bone002, ...)
        try:
            sample_folders = sorted([f for f in os.listdir(tissue_dir) 
                                   if os.path.isdir(os.path.join(tissue_dir, f))])
        except PermissionError:
            raise PermissionError(f"ERROR: Permission denied accessing {tissue_dir}")
        
        if len(sample_folders) == 0:
            raise ValueError(f"ERROR: No sample folders found in {tissue_dir}")
        
        # 각 조직별로 정확히 300개 샘플이 있어야 함
        if len(sample_folders) != 300:
            raise ValueError(f"ERROR: {tissue} has {len(sample_folders)} samples, expected 300")
        
        # split에 따라 샘플 선택
        selected_sample_folders = sample_folders[start_idx:end_idx]
        
        if len(selected_sample_folders) != expected_count:
            raise ValueError(f"ERROR: {tissue} has {len(selected_sample_folders)} {split} samples, expected {expected_count}")
        
        tissue_sample_count = 0
        for sample_folder in selected_sample_folders:
            sample_path = os.path.join(tissue_dir, sample_folder)
            
            # 샘플 폴더가 실제로 디렉토리인지 확인
            if not os.path.isdir(sample_path):
                raise ValueError(f"ERROR: {sample_path} is not a directory")
            
            # 5개 시간 게이트 이미지 존재 확인
            valid_gates = []
            missing_images = []
            for gate_idx in range(1, 6):  # _1.png to _5.png
                img_path = os.path.join(sample_path, f"{sample_folder}_{gate_idx}.png")
                if os.path.exists(img_path):
                    valid_gates.append(gate_idx)
                else:
                    missing_images.append(f"{sample_folder}_{gate_idx}.png")
            
            # 5개 게이트가 모두 있어야 함 - 없으면 오류 발생
            if len(valid_gates) != 5:
                error_msg = f"ERROR: {sample_folder} has only {len(valid_gates)}/5 images.\n"
                error_msg += f"  Missing images: {', '.join(missing_images)}\n"
                error_msg += f"  Path: {sample_path}"
                raise FileNotFoundError(error_msg)
            
            # 샘플 폴더가 비어있지 않은지 확인
            if not os.listdir(sample_path):
                raise ValueError(f"ERROR: {sample_path} is empty")
            
            props = tissue_properties[tissue]
            
            sample_info = {
                'sample_id': sample_folder,
                'tissue': tissue,
                'tissue_id': props['tissue_id'],
                'tissue_name_kr': props['name_kr'],
                'mu_a': props['mu_a'],
                'mu_s': props['mu_s'],
                'g': props['g'],
                'n': props['n'],
                'refractive_index': props['n'],  # 호환성을 위해 유지
                'base_path': f"{tissue}/{sample_folder}",
                'num_gates': 5,
                'split': split
            }
            
            dataset_info['samples'].append(sample_info)
            dataset_info['total_samples'] += 1
            tissue_sample_count += 1
        
        # 각 조직별로 정확히 expected_count개 샘플이 처리되었는지 확인
        if tissue_sample_count != expected_count:
            raise ValueError(f"ERROR: {tissue} processed {tissue_sample_count} {split} samples, expected {expected_count}")
    
    return dataset_info

def save_dataset_info(dataset_info, output_file):
    """데이터셋 정보를 JSON 파일로 저장합니다."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset_info, f, indent=2, ensure_ascii=False)
    
    split = dataset_info.get('split', 'unknown')
    print(f"{split.upper()} 데이터셋 정보가 {output_file}에 저장되었습니다.")
    return output_file

def print_dataset_summary(dataset_info):
    """데이터셋 요약 정보를 출력합니다."""
    split = dataset_info.get('split', 'unknown')
    print(f"\n=== {split.upper()} 데이터셋 요약 ===")
    print(f"데이터셋명: {dataset_info['dataset_name']}")
    print(f"총 샘플 수: {dataset_info['total_samples']}")
    print(f"조직 종류: {len(dataset_info['tissues'])}개")
    
    # 조직별 샘플 수
    tissue_counts = {}
    for sample in dataset_info['samples']:
        tissue = sample['tissue']
        tissue_counts[tissue] = tissue_counts.get(tissue, 0) + 1
    
    print("\n조직별 샘플 수:")
    for tissue, count in tissue_counts.items():
        props = dataset_info['tissue_properties'][tissue]
        print(f"  {tissue} ({props['name_kr']}, ID={props['tissue_id']}): {count}개")
        print(f"    μₐ={props['mu_a']}, μₛ={props['mu_s']}, g={props['g']}, n={props['n']}")
    
    # 굴절률 범위
    refractive_values = [sample['n'] for sample in dataset_info['samples']]
    if refractive_values:
        print(f"\n굴절률 범위: {min(refractive_values):.3f} ~ {max(refractive_values):.3f}")

if __name__ == "__main__":
    # 데이터셋 루트 디렉토리
    root_dir = r"C:\Users\user\Downloads\create data"
    
    # Train 라벨 정보 생성
    print("=" * 50)
    print("Train 데이터셋 라벨 정보 생성 중...")
    print("=" * 50)
    train_dataset_info = generate_dataset_labels(root_dir, split='train')
    print_dataset_summary(train_dataset_info)
    train_output_file = "dataset_labels_train.json"
    save_dataset_info(train_dataset_info, train_output_file)
    
    print("\n" + "=" * 50)
    print("Test 데이터셋 라벨 정보 생성 중...")
    print("=" * 50)
    test_dataset_info = generate_dataset_labels(root_dir, split='test')
    print_dataset_summary(test_dataset_info)
    test_output_file = "dataset_labels_test.json"
    save_dataset_info(test_dataset_info, test_output_file)
    
    print(f"\n{'=' * 50}")
    print(f"완료!")
    print(f"  - Train: {train_output_file}")
    print(f"  - Test: {test_output_file}")
    print(f"{'=' * 50}")
