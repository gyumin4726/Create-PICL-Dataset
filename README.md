# Temporal Dynamics Optical Dataset 생성 도구

시간 게이트 광학 산란 이미지를 사용한 조직 광학 특성 추정을 위한 데이터셋 생성 및 라벨링 도구입니다.

## 프로젝트 개요

이 프로젝트는 10가지 조직 타입의 시간 게이트 광학 산란 이미지 데이터셋을 train/test로 분할하고, 각 샘플의 광학 특성 정보를 포함한 라벨 파일을 생성합니다.

## 주요 기능

- **데이터셋 구조 생성**: 원본 데이터를 train/test 구조로 자동 분할 및 복사
- **라벨 파일 생성**: 각 샘플의 조직 타입 및 광학 특성 정보를 JSON 형식으로 생성

## 데이터셋 구조

### 조직 타입
데이터셋은 다음 10가지 조직 타입을 포함합니다:

| 조직 이름 | 한글명 | ID | μₐ | μₛ | g | n |
|---------|-------|-----|-----|-----|-----|-----|
| epidermis | 표피 | 0 | 0.03 | 10.0 | 0.90 | 1.40 |
| dermis | 진피 | 1 | 0.02 | 20.0 | 0.90 | 1.40 |
| subcutaneous_fat | 지방 조직 | 2 | 0.01 | 10.0 | 0.89 | 1.44 |
| muscle | 골격근 | 3 | 0.02 | 15.0 | 0.92 | 1.37 |
| cortical_bone | 피질골 | 4 | 0.015 | 20.0 | 0.90 | 1.50 |
| csf | 뇌척수액 | 5 | 0.0005 | 0.005 | 0.90 | 1.33 |
| gray_matter | 뇌 회색질 | 6 | 0.02 | 12.0 | 0.90 | 1.37 |
| white_matter | 뇌 백질 | 7 | 0.015 | 25.0 | 0.95 | 1.38 |
| whole_blood | 전혈 | 8 | 0.50 | 50.0 | 0.95 | 1.37 |
| tumor | 종양 조직 | 9 | 0.03 | 20.0 | 0.92 | 1.38 |

**광학 특성 설명:**
- **μₐ (mu_a)**: 흡수 계수 (Absorption coefficient)
- **μₛ (mu_s)**: 산란 계수 (Scattering coefficient)
- **g**: 비등방성 인자 (Anisotropy factor)
- **n**: 굴절률 (Refractive index)

### 샘플 구조
- 각 조직당 300개 샘플
- Train: 001-200번 샘플 (총 2,000개)
- Test: 201-300번 샘플 (총 1,000개)
- 각 샘플은 5개의 시간 게이트 이미지를 포함 (_1.png ~ _5.png)

### 시간 게이트
각 샘플은 5개의 시간 게이트 이미지를 포함합니다:
- gate_0: 0-1 ns
- gate_1: 1-2 ns
- gate_2: 2-3 ns
- gate_3: 3-4 ns
- gate_4: 4-5 ns

## 파일 구조

```
create data/
├── create_dataset_structure.py    # 데이터셋 구조 생성 스크립트
├── generate_labels.py             # 라벨 파일 생성 스크립트
├── DATASET/                       # 데이터셋 폴더 (생성됨)
│   ├── train/
│   │   ├── epidermis/
│   │   ├── dermis/
│   │   └── ...
│   └── test/
│       ├── epidermis/
│       ├── dermis/
│       └── ...
├── dataset_labels_train.json      # Train 라벨 파일 (생성됨)
└── dataset_labels_test.json       # Test 라벨 파일 (생성됨)
```

## 사용 방법

### 1. 데이터셋 구조 생성

`create_dataset_structure.py`를 실행하여 원본 데이터를 train/test 구조로 분할하고 복사합니다.

```bash
python create_dataset_structure.py
```

**기능:**
- DATASET 폴더 안에 train/test 디렉토리 생성
- 각 조직별로 샘플 001-200을 train으로, 201-300을 test로 복사
- 이미지 파일만 복사 (JSON 파일 제외)

**주의사항:**
- 스크립트 내부의 `source_dir`와 `dataset_dir` 경로를 실제 경로로 수정해야 합니다.
- 각 조직 폴더에는 정확히 300개의 샘플 폴더가 있어야 합니다.

### 2. 라벨 파일 생성

`generate_labels.py`를 실행하여 train/test 데이터셋의 라벨 파일을 생성합니다.

```bash
python generate_labels.py
```

**생성되는 파일:**
- `dataset_labels_train.json`: Train 데이터셋 라벨 정보
- `dataset_labels_test.json`: Test 데이터셋 라벨 정보

**라벨 파일 구조:**
```json
{
  "dataset_name": "Temporal_Dynamics_Optical_Dataset_Train",
  "description": "...",
  "split": "train",
  "total_samples": 2000,
  "tissues": [...],
  "tissue_properties": {...},
  "time_gates": {...},
  "samples": [
    {
      "sample_id": "epidermis001",
      "tissue": "epidermis",
      "tissue_id": 0,
      "tissue_name_kr": "표피",
      "mu_a": 0.03,
      "mu_s": 10.0,
      "g": 0.90,
      "n": 1.40,
      "refractive_index": 1.40,
      "base_path": "epidermis/epidermis001",
      "num_gates": 5,
      "split": "train"
    },
    ...
  ]
}
```

**주의사항:**
- 스크립트 내부의 `root_dir` 경로를 실제 경로로 수정해야 합니다.
- 각 샘플 폴더에는 5개의 시간 게이트 이미지가 모두 존재해야 합니다.

## 요구사항

- Python 3.x
- 표준 라이브러리만 사용 (별도 설치 패키지 없음)

## 주의사항

1. **경로 설정**: 각 스크립트의 경로 변수를 실행 환경에 맞게 수정해야 합니다.
2. **데이터 검증**: 
   - 각 조직당 정확히 300개의 샘플이 있어야 합니다.
   - 각 샘플 폴더에는 5개의 시간 게이트 이미지가 모두 존재해야 합니다.
3. **파일 복사**: `create_dataset_structure.py`는 이미지 파일만 복사하며, JSON 파일은 수동으로 옮겨야 합니다.

## 출력 파일

### dataset_labels_train.json
Train 데이터셋 (2,000개 샘플)의 라벨 정보를 포함합니다.

### dataset_labels_test.json
Test 데이터셋 (1,000개 샘플)의 라벨 정보를 포함합니다.

## 라이선스

프로젝트 라이선스 정보를 여기에 추가하세요.



