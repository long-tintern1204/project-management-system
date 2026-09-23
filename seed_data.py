"""
Script nạp dữ liệu mẫu (Seed Data) cho hệ thống Quản lý dự án.
Chạy bằng lệnh: python seed_data.py
"""

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import Base, SessionLocal, engine
from app.core.security import get_password_hash
from app.models import Project, TechTag, User


SAMPLE_PROJECTS = [
    {
        "customer_name": "株式会社みずほフィナンシャル",
        "project_name": "次世代バンキングAPI基盤構築",
        "description": "勘定系システムと外部FinTechサービスを連携するための高信頼・低遅延API Gatewayの設計および構築プロジェクト。",
        "start_date": "2025-04-01",
        "end_date": "2026-03-31",
        "is_ongoing": False,
        "team_size": 12,
        "total_man_month": 72.0,
        "source_note": "金融系プライムSIer経由での受注",
        "industry": "金融・保険",
        "outcome_note": "API応答時間を従来の30%短縮し、月間2,000万リクエストを安定処理達成。",
        "team_composition_note": "PM: 1, TechLead: 1, Backend: 6, QA: 2, DevOps: 2",
        "technologies": ["Java", "Spring Boot", "AWS", "PostgreSQL", "Docker", "Terraform"],
        "project_types": ["offshore", "new_dev"],
        "dev_process_phases": ["requirements", "design", "implementation", "testing", "release"],
    },
    {
        "customer_name": "楽天グループ株式会社",
        "project_name": "ECモール向けレコメンドエンジン刷新",
        "description": "ユーザーの閲覧履歴と購買行動を機械学習モデルでリアルタイム分析し、最適なレコメンド商品を提示するマイクロサービスの開発。",
        "start_date": "2025-06-01",
        "end_date": None,
        "is_ongoing": True,
        "team_size": 8,
        "total_man_month": 48.0,
        "source_note": "既存取引先からの追加案件",
        "industry": "Eコマース・小売り",
        "outcome_note": "CVR（購買転換率）が前年比15%向上。",
        "team_composition_note": "PM: 1, DataScientist: 2, ML Engineer: 3, Frontend: 2",
        "technologies": ["Python", "FastAPI", "Kubernetes", "Redis", "TensorFlow", "React"],
        "project_types": ["lab", "new_dev"],
        "dev_process_phases": ["design", "implementation", "testing"],
    },
    {
        "customer_name": "トヨタ自動車株式会社",
        "project_name": "コネクテッドカーテレマティクス基盤保守",
        "description": "車載通信機からリアルタイムに送信される車両運行データの蓄積・可視化ダッシュボードの機能改善および運用保守。",
        "start_date": "2024-01-01",
        "end_date": None,
        "is_ongoing": True,
        "team_size": 5,
        "total_man_month": 60.0,
        "source_note": "継続保守契約",
        "industry": "製造・自動車",
        "outcome_note": "SLA 99.99%達成、障害対応時間を平均15分に短縮。",
        "team_composition_note": "PL: 1, Backend: 2, Infrastructure: 2",
        "technologies": ["Go", "TypeScript", "AWS", "Kafka", "MySQL"],
        "project_types": ["maintenance", "ses"],
        "dev_process_phases": ["maintenance_ops"],
    },
    {
        "customer_name": "株式会社リクルート",
        "project_name": "求人マッチングAIプラットフォーム",
        "description": "求職者のスキルシートと求人要件のセマンティック検索を行い、最適なマッチングを実現するSaaS型プロダクト。",
        "start_date": "2025-02-01",
        "end_date": "2025-11-30",
        "is_ongoing": False,
        "team_size": 10,
        "total_man_month": 50.0,
        "source_note": "コンペ提案により受注",
        "industry": "人材・メディア",
        "outcome_note": "スカウト送信後の返信率が22%から38%に改善。",
        "team_composition_note": "PM: 1, Frontend: 3, Backend: 4, QA: 2",
        "technologies": ["Next.js", "TypeScript", "Python", "OpenAI API", "PostgreSQL"],
        "project_types": ["offshore", "new_dev"],
        "dev_process_phases": ["requirements", "design", "implementation", "testing", "release"],
    },
    {
        "customer_name": "エムスリー株式会社",
        "project_name": "医師向けオンライン診療支援システム",
        "description": "WebRTCを活用した医師と患者間のリアルタイムビデオ通話および電子カルテ連携システム。",
        "start_date": "2024-09-01",
        "end_date": "2025-08-31",
        "is_ongoing": False,
        "team_size": 7,
        "total_man_month": 42.0,
        "source_note": "医療ITコンソーシアム経由",
        "industry": "医療・ヘルスケア",
        "outcome_note": "全国200以上のクリニックで導入完了。",
        "team_composition_note": "PM: 1, Fullstack: 4, QA: 2",
        "technologies": ["React", "Node.js", "WebRTC", "Docker", "GCP"],
        "project_types": ["offshore", "new_dev"],
        "dev_process_phases": ["design", "implementation", "testing", "release"],
    },
    {
        "customer_name": "ヤマト運輸株式会社",
        "project_name": "配送ルート最適化アルゴリズム開発",
        "description": "交通状況、天候、荷物量からラストワンマイル配送の最短ルートを動的に計算するモバイルアプリおよびバックエンド。",
        "start_date": "2025-05-01",
        "end_date": None,
        "is_ongoing": True,
        "team_size": 6,
        "total_man_month": 36.0,
        "source_note": "物流DXイノベーション公募",
        "industry": "運輸・物流",
        "outcome_note": "ドライバーの走行距離を日平均12%削減。",
        "team_composition_note": "Lead: 1, Algorithm: 2, Mobile: 2, Backend: 1",
        "technologies": ["Flutter", "Python", "FastAPI", "PostgreSQL", "Google Maps API"],
        "project_types": ["lab", "new_dev"],
        "dev_process_phases": ["requirements", "design", "implementation"],
    },
    {
        "customer_name": "ベネッセコーポレーション",
        "project_name": "小学生向けインタラクティブ学習タブレットアプリ",
        "description": "ゲーミフィケーションを取り入れた算数・英語学習用ネイティブアプリのUI刷新と教材管理CMS開発。",
        "start_date": "2024-06-01",
        "end_date": "2025-03-31",
        "is_ongoing": False,
        "team_size": 9,
        "total_man_month": 54.0,
        "source_note": "教育系代理店からの紹介",
        "industry": "教育・EdTech",
        "outcome_note": "子供の継続学習日数が前バージョン比で40%増加。",
        "team_composition_note": "PM: 1, Unity: 3, Backend: 3, Designer: 2",
        "technologies": ["Unity", "C#", "Node.js", "Vue.js", "MySQL"],
        "project_types": ["offshore", "new_dev"],
        "dev_process_phases": ["requirements", "design", "implementation", "testing", "release"],
    },
    {
        "customer_name": "三菱地所株式会社",
        "project_name": "スマートビルIoT管理統合ポータル",
        "description": "商業ビル内の空調、照明、入退館ゲートのセンサーデータを一元集約し、省エネ自動制御を行うIoTプラットフォーム。",
        "start_date": "2025-01-15",
        "end_date": None,
        "is_ongoing": True,
        "team_size": 8,
        "total_man_month": 40.0,
        "source_note": "不動産テック案件",
        "industry": "不動産・建設",
        "outcome_note": "年間電力消費量8%削減の見込み。",
        "team_composition_note": "PM: 1, IoT: 2, Backend: 3, Frontend: 2",
        "technologies": ["Vue.js", "Python", "AWS IoT Core", "TimescaleDB", "Docker"],
        "project_types": ["lab", "new_dev"],
        "dev_process_phases": ["requirements", "design", "implementation", "testing"],
    },
    {
        "customer_name": "東京海上日動火災保険",
        "project_name": "自動車事故AI画像鑑定システム",
        "description": "事故車両の写真から損傷箇所と損傷度合いをAIが自動判別し、保険金見積もりを自動生成するシステム。",
        "start_date": "2024-10-01",
        "end_date": "2025-09-30",
        "is_ongoing": False,
        "team_size": 6,
        "total_man_month": 36.0,
        "source_note": "AIコンペ最優秀賞からの商用化",
        "industry": "金融・保険",
        "outcome_note": "査定にかかる日数を7日から1日に短縮。",
        "team_composition_note": "PM: 1, ML Engineer: 2, Backend: 2, QA: 1",
        "technologies": ["PyTorch", "Python", "FastAPI", "React", "AWS"],
        "project_types": ["offshore", "new_dev"],
        "dev_process_phases": ["requirements", "design", "implementation", "testing", "release"],
    },
    {
        "customer_name": "ソニー株式会社",
        "project_name": "エンタメ配信サービス向け課金・決済マイクロサービス",
        "description": "グローバル展開するストリーミングサービスの多通貨対応、サブスクリプション決済基盤の設計・開発。",
        "start_date": "2025-03-01",
        "end_date": None,
        "is_ongoing": True,
        "team_size": 11,
        "total_man_month": 66.0,
        "source_note": "グローバル共通プラットフォーム案件",
        "industry": "情報通信・エンタメ",
        "outcome_note": "カード決済成功率99.8%維持、チャージバック詐欺を激減。",
        "team_composition_note": "Lead: 2, Backend: 6, Security: 1, QA: 2",
        "technologies": ["Go", "gRPC", "Kubernetes", "PostgreSQL", "Stripe API"],
        "project_types": ["offshore", "new_dev"],
        "dev_process_phases": ["design", "implementation", "testing"],
    },
    {
        "customer_name": "パナソニックホールディングス",
        "project_name": "スマート家電遠隔操作モバイルアプリ開発",
        "description": "エアコン、冷蔵庫、洗濯機などのIoT家電を遠隔操作・モニタリングするiOS/Android共通アプリ。",
        "start_date": "2024-04-01",
        "end_date": "2025-01-31",
        "is_ongoing": False,
        "team_size": 8,
        "total_man_month": 48.0,
        "source_note": "家電事業部直接案件",
        "industry": "製造・電機",
        "outcome_note": "AppStoreレビュー平均4.4点達成、DL数100万突破。",
        "team_composition_note": "PM: 1, Flutter: 4, Backend: 2, UI/UX: 1",
        "technologies": ["Flutter", "Dart", "AWS", "MQTT", "Node.js"],
        "project_types": ["offshore", "new_dev"],
        "dev_process_phases": ["requirements", "design", "implementation", "testing", "release"],
    },
    {
        "customer_name": "株式会社ファーストリテイリング",
        "project_name": "店舗在庫リアルタイム追跡RFID連携システム",
        "description": "全店舗のRFIDリーダーから集約される商品棚卸・移動データを秒単位で反映する在庫同期基盤。",
        "start_date": "2025-07-01",
        "end_date": None,
        "is_ongoing": True,
        "team_size": 7,
        "total_man_month": 35.0,
        "source_note": "アパレルDX戦略案件",
        "industry": "Eコマース・小売り",
        "outcome_note": "棚卸業務時間を各店舗あたり70%削減。",
        "team_composition_note": "PL: 1, Backend: 4, Cloud: 2",
        "technologies": ["Java", "Spring Boot", "Kafka", "Redis", "MySQL"],
        "project_types": ["ses", "new_dev"],
        "dev_process_phases": ["design", "implementation"],
    },
    {
        "customer_name": "日本航空株式会社 (JAL)",
        "project_name": "フライトクルー勤務スケジューリング最適化",
        "description": "航空法規制、パイロットの保有資格、休暇希望を考慮した月次シフトスケジューリングの数理最適化システム。",
        "start_date": "2024-08-01",
        "end_date": "2025-05-31",
        "is_ongoing": False,
        "team_size": 5,
        "total_man_month": 25.0,
        "source_note": "航空運行システム刷新案件",
        "industry": "運輸・航空",
        "outcome_note": "手動シフト作成時間を月120時間から3時間に短縮。",
        "team_composition_note": "PM: 1, Optimization: 2, Frontend: 1, Backend: 1",
        "technologies": ["Python", "FastAPI", "React", "TypeScript", "Docker"],
        "project_types": ["offshore", "new_dev"],
        "dev_process_phases": ["requirements", "design", "implementation", "testing", "release"],
    },
    {
        "customer_name": "味の素株式会社",
        "project_name": "グローバルサプライチェーン需給予測ポータル",
        "description": "世界15カ国の工場・物流拠点における原材料在庫および製品需要を予測し、発注を自動推奨するシステム。",
        "start_date": "2025-02-15",
        "end_date": None,
        "is_ongoing": True,
        "team_size": 9,
        "total_man_month": 45.0,
        "source_note": "基幹システム連携プロジェクト",
        "industry": "食品・消費財",
        "outcome_note": "廃棄ロスを前年同期比で18%削減。",
        "team_composition_note": "PM: 1, Data: 3, Backend: 3, Frontend: 2",
        "technologies": ["Python", "Vue.js", "Azure", "Snowflake", "FastAPI"],
        "project_types": ["lab", "new_dev"],
        "dev_process_phases": ["requirements", "design", "implementation"],
    },
    {
        "customer_name": "ソフトバンク株式会社",
        "project_name": "5G基地局監視・自動障害復旧エージェント",
        "description": "全国の基地局ログを監視し、軽微な障害発生時にAIエージェントが自動で再起動やトラフィック迂回を実行するシステム。",
        "start_date": "2024-05-01",
        "end_date": "2025-02-28",
        "is_ongoing": False,
        "team_size": 10,
        "total_man_month": 50.0,
        "source_note": "通信ネットワーク自動化プロジェクト",
        "industry": "情報通信・インフラ",
        "outcome_note": "深夜の人的一次対応インシデント数を80%削減。",
        "team_composition_note": "PM: 1, Network: 3, Backend: 4, QA: 2",
        "technologies": ["Go", "Python", "Kubernetes", "Prometheus", "Elasticsearch"],
        "project_types": ["offshore", "new_dev"],
        "dev_process_phases": ["requirements", "design", "implementation", "testing", "release"],
    },
    {
        "customer_name": "森ビル株式会社",
        "project_name": "デジタルサイネージ広告配信CMS保守",
        "description": "都市型複合施設内の大型ビジョンおよびフロア案内サイネージへの広告スケジュール配信と稼働監視。",
        "start_date": "2024-01-01",
        "end_date": None,
        "is_ongoing": True,
        "team_size": 4,
        "total_man_month": 48.0,
        "source_note": "既存CMS長期保守案件",
        "industry": "不動産・広告",
        "outcome_note": "緊急告知テロップのリアルタイム配信機能を新規追加。",
        "team_composition_note": "Lead: 1, Frontend: 1, Backend: 1, Support: 1",
        "technologies": ["React", "Node.js", "AWS S3", "CloudFront", "PostgreSQL"],
        "project_types": ["maintenance", "ses"],
        "dev_process_phases": ["maintenance_ops"],
    },
    {
        "customer_name": "株式会社サイバーエージェント",
        "project_name": "アドテク向けリアルタイム入札(RTB)エンジン最適化",
        "description": "ミリ秒単位でオークションを行うDSP/SSPシステムのレイテンシ低減とインメモリキャッシュ最適化。",
        "start_date": "2025-04-10",
        "end_date": None,
        "is_ongoing": True,
        "team_size": 6,
        "total_man_month": 30.0,
        "source_note": "技術顧問経由での参画",
        "industry": "インターネット・広告",
        "outcome_note": "P99レイテンシを12msから7msに高速化。",
        "team_composition_note": "TechLead: 1, Rust: 3, Infrastructure: 2",
        "technologies": ["Rust", "C++", "Redis", "Kafka", "GCP"],
        "project_types": ["ses", "new_dev"],
        "dev_process_phases": ["design", "implementation", "testing"],
    },
    {
        "customer_name": "クックパッド株式会社",
        "project_name": "レシピ推薦パーソナライズ基盤リファクタリング",
        "description": "モノリス構成からマイクロサービスアーキテクチャへの段階的移行およびGraphQL Gateway導入。",
        "start_date": "2024-11-01",
        "end_date": "2025-06-30",
        "is_ongoing": False,
        "team_size": 5,
        "total_man_month": 25.0,
        "source_note": "Webサービス近代化支援",
        "industry": "インターネット・Webサービス",
        "outcome_note": "デプロイ頻度が週1回から1日複数回に向上。",
        "team_composition_note": "Lead: 1, Backend: 3, Frontend: 1",
        "technologies": ["Ruby", "TypeScript", "GraphQL", "Docker", "AWS"],
        "project_types": ["offshore", "new_dev"],
        "dev_process_phases": ["design", "implementation", "testing", "release"],
    },
    {
        "customer_name": "任天堂株式会社",
        "project_name": "ゲーム配信プラットフォーム基盤拡張",
        "description": "全世界数千万人のアクティブユーザーを支えるオンラインストアおよびセーブデータクラウド同期サービスの負荷分散基盤刷新。",
        "start_date": "2024-07-01",
        "end_date": "2025-04-30",
        "is_ongoing": False,
        "team_size": 14,
        "total_man_month": 84.0,
        "source_note": "エンターテインメント基盤公募",
        "industry": "ゲーム・エンタメ",
        "outcome_note": "新作リリース時の同時接続アクセススパイクをゼロダウンタイムで処理達成。",
        "team_composition_note": "Lead: 2, Backend: 8, Infrastructure: 3, QA: 1",
        "technologies": ["Go", "AWS", "DynamoDB", "Redis", "Docker", "Terraform"],
        "project_types": ["offshore", "new_dev"],
        "dev_process_phases": ["requirements", "design", "implementation", "testing", "release"],
    },
    {
        "customer_name": "LINEヤフー株式会社",
        "project_name": "法人向け公式アカウントCRM連携モジュール",
        "description": "LINE公式アカウントと顧客企業の既存CRMシステム（Salesforce等）をリアルタイム双方向連携するWebhook中継基盤の設計・開発。",
        "start_date": "2025-05-15",
        "end_date": None,
        "is_ongoing": True,
        "team_size": 7,
        "total_man_month": 42.0,
        "source_note": "SaaSプラットフォーム連携案件",
        "industry": "IT・通信",
        "outcome_note": "メッセージ配信遅延を平均0.5秒未満に抑え、APIスループットを3倍に強化。",
        "team_composition_note": "PM: 1, Backend: 4, Frontend: 1, DevOps: 1",
        "technologies": ["TypeScript", "Next.js", "Node.js", "Kafka", "MySQL", "Docker"],
        "project_types": ["lab", "new_dev"],
        "dev_process_phases": ["requirements", "design", "implementation", "testing"],
    },
]


def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        print("🌱 Seeding data...")

        # 1. Tạo user demo/admin mẫu nếu chưa có
        default_users = [
            {"email": "admin@gmail.com", "password": "AdminPass123@", "role": "admin"},
            {"email": "admin@example.com", "password": "Password123", "role": "admin"},
        ]
        for u in default_users:
            user = db.scalar(select(User).where(User.email == u["email"]))
            if not user:
                user = User(
                    email=u["email"],
                    password_hash=get_password_hash(u["password"]),
                    role=u["role"],
                )
                db.add(user)
                db.commit()
                print(f"  ✓ Created user: {u['email']} (Password: {u['password']})")
            else:
                # Cập nhật lại mật khẩu chuẩn nếu đã tồn tại
                user.password_hash = get_password_hash(u["password"])
                db.commit()
                print(f"  ✓ Updated user password: {u['email']}")

        admin_email = "admin@gmail.com"

        # 2. Xử lý TechTag và nạp Projects
        all_tags = set()
        for p in SAMPLE_PROJECTS:
            for tag in p["technologies"]:
                all_tags.add(tag.strip())

        # Thêm các tag mới vào DB
        existing_tags = set(db.scalars(select(TechTag.name)).all())
        new_tags = all_tags - existing_tags
        for tag_name in new_tags:
            db.add(TechTag(name=tag_name))
        db.commit()
        print(f"  ✓ Synchronized {len(all_tags)} unique tech tags (added {len(new_tags)} new tags)")

        # 3. Nạp Projects
        added_count = 0
        for p_data in SAMPLE_PROJECTS:
            # Kiểm tra xem dự án đã tồn tại chưa (tránh nạp trùng khi chạy nhiều lần)
            exists = db.scalar(
                select(Project).where(
                    Project.customer_name == p_data["customer_name"],
                    Project.project_name == p_data["project_name"],
                    Project.deleted_at.is_(None),
                )
            )
            if exists:
                continue

            project = Project(
                customer_name=p_data["customer_name"],
                project_name=p_data["project_name"],
                description=p_data["description"],
                start_date=p_data["start_date"],
                end_date=p_data["end_date"],
                is_ongoing=p_data["is_ongoing"],
                team_size=p_data["team_size"],
                total_man_month=p_data["total_man_month"],
                source_note=p_data["source_note"],
                industry=p_data["industry"],
                outcome_note=p_data["outcome_note"],
                team_composition_note=p_data["team_composition_note"],
                technologies_csv=",".join(p_data["technologies"]),
                project_types_csv=",".join(p_data["project_types"]),
                dev_process_phases_csv=",".join(p_data["dev_process_phases"]),
                created_by=admin_email,
            )
            db.add(project)
            added_count += 1

        db.commit()
        print(f"  ✓ Added {added_count} projects into database.")
        print("🎉 Seed data completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error while seeding data: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed()