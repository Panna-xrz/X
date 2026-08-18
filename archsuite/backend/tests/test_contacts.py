"""联系单 API 测试：委方 / 小组联系人 CRUD + 按类型过滤。"""

from httpx import AsyncClient


async def _create_project(client: AsyncClient) -> int:
    """创建测试项目并返回 ID。"""
    resp = await client.post("/api/v1/projects", json={"name": "项目C", "code": "PC"})
    assert resp.status_code == 201
    return resp.json()["id"]


async def _create_contact(
    client: AsyncClient,
    project_id: int,
    name: str,
    contact_type: str = "client",
    role: str | None = None,
) -> int:
    """创建联系人并返回 ID。"""
    payload: dict = {"projectId": project_id, "contactType": contact_type, "name": name}
    if role is not None:
        payload["role"] = role
    resp = await client.post("/api/v1/contacts", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()["id"]


async def test_client_contact_crud(client: AsyncClient) -> None:
    """委方联系人 CRUD 全流程：创建-详情-更新-删除。"""
    pid = await _create_project(client)
    cid = await _create_contact(client, pid, "张总", "client", "甲方代表")

    # 详情：contactType 别名输出
    resp = await client.get(f"/api/v1/contacts/{cid}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "张总"
    assert data["contactType"] == "client"
    assert data["role"] == "甲方代表"
    assert data["projectId"] == pid
    assert "createdAt" in data

    # 更新（仅传部分字段）
    resp = await client.put(
        f"/api/v1/contacts/{cid}", json={"phone": "13800000000", "role": "项目总监"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["phone"] == "13800000000"
    assert data["role"] == "项目总监"
    assert data["name"] == "张总"  # 未传字段保持不变

    # 删除
    resp = await client.delete(f"/api/v1/contacts/{cid}")
    assert resp.status_code == 204
    resp = await client.get(f"/api/v1/contacts/{cid}")
    assert resp.status_code == 404


async def test_team_contact_crud(client: AsyncClient) -> None:
    """小组联系人 CRUD + 类型切换。"""
    pid = await _create_project(client)
    cid = await _create_contact(client, pid, "李工", "team", "建筑专业")

    resp = await client.get(f"/api/v1/contacts/{cid}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["contactType"] == "team"
    assert data["role"] == "建筑专业"

    # 更新联系单类型（team → client）
    resp = await client.put(f"/api/v1/contacts/{cid}", json={"contactType": "client"})
    assert resp.status_code == 200
    assert resp.json()["contactType"] == "client"


async def test_contact_filter_by_type(client: AsyncClient) -> None:
    """按 contactType 过滤联系人列表。"""
    pid = await _create_project(client)
    # 创建 2 个委方 + 1 个小组
    await _create_contact(client, pid, "委方A", "client")
    await _create_contact(client, pid, "委方B", "client")
    await _create_contact(client, pid, "小组成员X", "team")

    # 全量
    resp = await client.get(f"/api/v1/contacts?projectId={pid}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 3
    assert len(data["list"]) == 3

    # 仅委方
    resp = await client.get(f"/api/v1/contacts?projectId={pid}&contactType=client")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert len(data["list"]) == 2
    assert all(c["contactType"] == "client" for c in data["list"])

    # 仅小组
    resp = await client.get(f"/api/v1/contacts?projectId={pid}&contactType=team")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["list"][0]["contactType"] == "team"


async def test_contact_default_type_is_client(client: AsyncClient) -> None:
    """未传 contactType 时默认为 client。"""
    pid = await _create_project(client)
    resp = await client.post(
        "/api/v1/contacts",
        json={"projectId": pid, "name": "默认委方"},
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["contactType"] == "client"


async def test_contact_create_missing_project_404(client: AsyncClient) -> None:
    """为不存在的项目创建联系人应返回 404。"""
    resp = await client.post(
        "/api/v1/contacts",
        json={"projectId": 99999, "contactType": "client", "name": "无效"},
    )
    assert resp.status_code == 404


async def test_contact_list_missing_project_404(client: AsyncClient) -> None:
    """查询不存在项目的联系人应返回 404。"""
    resp = await client.get("/api/v1/contacts?projectId=99999")
    assert resp.status_code == 404
