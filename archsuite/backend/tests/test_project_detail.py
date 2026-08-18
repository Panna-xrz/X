"""项目详细信息 API 测试：指标 / 场地周边 / 物理环境 / 人文环境 upsert + 建筑单体 CRUD。"""

from httpx import AsyncClient


async def _create_project(client: AsyncClient) -> int:
    """创建测试项目并返回 ID。"""
    resp = await client.post("/api/v1/projects", json={"name": "项目D", "code": "PD"})
    assert resp.status_code == 201
    return resp.json()["id"]


# ========== 指标信息 ==========

async def test_metric_upsert(client: AsyncClient) -> None:
    """指标信息 upsert：创建 + 更新 + 查询。"""
    pid = await _create_project(client)
    # 创建
    resp = await client.put(
        f"/api/v1/projects/{pid}/metric",
        json={
            "projectId": pid,
            "landUse": "居住用地",
            "siteArea": 10000.5,
            "farAbove": 2.5,
            "greenRatio": 35.0,
            "parkingAbove": 100,
            "parkingUnder": 200,
            "remarks": "首次指标",
        },
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["projectId"] == pid
    assert data["landUse"] == "居住用地"
    assert data["siteArea"] == 10000.5
    assert data["parkingAbove"] == 100

    # 更新（同 project_id，触发 update 分支）
    resp = await client.put(
        f"/api/v1/projects/{pid}/metric",
        json={
            "projectId": pid,
            "landUse": "商业用地",
            "siteArea": 15000.0,
            "farAbove": 3.0,
            "greenRatio": 30.0,
            "parkingAbove": 150,
            "parkingUnder": 250,
            "remarks": "更新指标",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["landUse"] == "商业用地"
    assert data["siteArea"] == 15000.0
    assert data["parkingAbove"] == 150
    assert data["remarks"] == "更新指标"

    # GET 验证
    resp = await client.get(f"/api/v1/projects/{pid}/metric")
    assert resp.status_code == 200
    assert resp.json()["landUse"] == "商业用地"


async def test_metric_get_not_found(client: AsyncClient) -> None:
    """未创建指标时 GET 返回 404；不存在项目也 404。"""
    pid = await _create_project(client)
    resp = await client.get(f"/api/v1/projects/{pid}/metric")
    assert resp.status_code == 404

    resp = await client.get("/api/v1/projects/99999/metric")
    assert resp.status_code == 404


async def test_metric_upsert_missing_project_404(client: AsyncClient) -> None:
    """为不存在的项目 upsert 指标应返回 404。"""
    resp = await client.put(
        "/api/v1/projects/99999/metric",
        json={"projectId": 99999, "siteArea": 1000.0},
    )
    assert resp.status_code == 404


# ========== 场地周边 ==========

async def test_surrounding_upsert(client: AsyncClient) -> None:
    """场地周边 upsert：创建 + 更新（全量替换语义）。"""
    pid = await _create_project(client)
    resp = await client.put(
        f"/api/v1/projects/{pid}/surrounding",
        json={
            "projectId": pid,
            "longitude": 116.404,
            "latitude": 39.915,
            "nearbyRoads": "长安街",
            "transitInfo": "地铁1号线",
            "remarks": "首次",
        },
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["longitude"] == 116.404
    assert data["nearbyRoads"] == "长安街"
    assert data["transitInfo"] == "地铁1号线"

    # 更新：未传字段被置空（upsert 全量替换语义）
    resp = await client.put(
        f"/api/v1/projects/{pid}/surrounding",
        json={
            "projectId": pid,
            "longitude": 121.473,
            "latitude": 31.230,
            "nearbyRoads": "南京路",
            "remarks": "更新",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["longitude"] == 121.473
    assert data["nearbyRoads"] == "南京路"
    assert data["transitInfo"] is None  # 全量替换：未传字段置空

    # GET 验证
    resp = await client.get(f"/api/v1/projects/{pid}/surrounding")
    assert resp.status_code == 200
    assert resp.json()["nearbyRoads"] == "南京路"


# ========== 物理环境 ==========

async def test_physical_upsert(client: AsyncClient) -> None:
    """物理环境 upsert：创建 + 更新。"""
    pid = await _create_project(client)
    resp = await client.put(
        f"/api/v1/projects/{pid}/physical",
        json={
            "projectId": pid,
            "climateZone": "寒冷地区",
            "prevailingWind": "西北风",
            "annualPrecipitation": 600.0,
            "avgAnnualTemp": 12.5,
            "remarks": "首次",
        },
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["climateZone"] == "寒冷地区"
    assert data["avgAnnualTemp"] == 12.5

    # 更新
    resp = await client.put(
        f"/api/v1/projects/{pid}/physical",
        json={
            "projectId": pid,
            "climateZone": "夏热冬冷地区",
            "prevailingWind": "东南风",
            "annualPrecipitation": 1200.0,
            "avgAnnualTemp": 18.0,
            "remarks": "更新",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["climateZone"] == "夏热冬冷地区"
    assert data["annualPrecipitation"] == 1200.0

    # GET 验证
    resp = await client.get(f"/api/v1/projects/{pid}/physical")
    assert resp.status_code == 200
    assert resp.json()["climateZone"] == "夏热冬冷地区"


# ========== 人文环境 ==========

async def test_cultural_upsert(client: AsyncClient) -> None:
    """人文环境 upsert：创建 + 更新。"""
    pid = await _create_project(client)
    resp = await client.put(
        f"/api/v1/projects/{pid}/cultural",
        json={
            "projectId": pid,
            "culturalSymbols": "徽派建筑",
            "regionalArchitecture": "马头墙",
            "urbanColorScheme": "粉墙黛瓦",
            "remarks": "首次",
        },
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["culturalSymbols"] == "徽派建筑"

    # 更新
    resp = await client.put(
        f"/api/v1/projects/{pid}/cultural",
        json={
            "projectId": pid,
            "culturalSymbols": "京派建筑",
            "regionalArchitecture": "四合院",
            "urbanColorScheme": "灰砖青瓦",
            "localCustoms": "北京习俗",
            "historicalCulture": "燕京文化",
            "remarks": "更新",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["culturalSymbols"] == "京派建筑"
    assert data["historicalCulture"] == "燕京文化"

    # GET 验证
    resp = await client.get(f"/api/v1/projects/{pid}/cultural")
    assert resp.status_code == 200
    assert resp.json()["culturalSymbols"] == "京派建筑"


# ========== 建筑单体 ==========

async def test_building_crud_flow(client: AsyncClient) -> None:
    """建筑单体 CRUD 全流程：创建-列表-详情-更新-删除。"""
    pid = await _create_project(client)

    # 创建
    resp = await client.post(
        f"/api/v1/projects/{pid}/buildings",
        json={
            "projectId": pid,
            "code": "B-01",
            "name": "1号楼",
            "buildingNature": "住宅",
            "buildingFunction": "居住",
            "floorsAbove": 18,
            "floorsUnder": 2,
            "height": 54.0,
            "floorArea": 10000.0,
            "remarks": "住宅楼",
        },
    )
    assert resp.status_code == 201, resp.text
    building = resp.json()
    assert building["name"] == "1号楼"
    assert building["projectId"] == pid
    assert building["floorsAbove"] == 18
    bid = building["id"]

    # 再创建一个，验证列表多元素
    resp = await client.post(
        f"/api/v1/projects/{pid}/buildings",
        json={"projectId": pid, "code": "B-02", "name": "2号楼"},
    )
    assert resp.status_code == 201

    # 列表（按 id 升序）
    resp = await client.get(f"/api/v1/projects/{pid}/buildings")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 2
    assert items[0]["name"] == "1号楼"
    assert items[1]["name"] == "2号楼"

    # 详情
    resp = await client.get(f"/api/v1/projects/{pid}/buildings/{bid}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "1号楼"

    # 更新（仅传部分字段）
    resp = await client.put(
        f"/api/v1/projects/{pid}/buildings/{bid}",
        json={"height": 60.0, "remarks": "加层后"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["height"] == 60.0
    assert data["remarks"] == "加层后"
    assert data["name"] == "1号楼"  # 未传字段保持不变

    # 删除
    resp = await client.delete(f"/api/v1/projects/{pid}/buildings/{bid}")
    assert resp.status_code == 204
    resp = await client.get(f"/api/v1/projects/{pid}/buildings/{bid}")
    assert resp.status_code == 404


async def test_building_create_missing_project_404(client: AsyncClient) -> None:
    """为不存在的项目创建建筑单体应返回 404。"""
    resp = await client.post(
        "/api/v1/projects/99999/buildings",
        json={"projectId": 99999, "name": "无效楼"},
    )
    assert resp.status_code == 404


async def test_buildings_list_missing_project_404(client: AsyncClient) -> None:
    """查询不存在项目的建筑列表应返回 404。"""
    resp = await client.get("/api/v1/projects/99999/buildings")
    assert resp.status_code == 404
