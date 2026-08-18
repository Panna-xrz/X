"""API 集成测试：健康检查与核心资源 CRUD 流程。"""


async def test_health(client: AsyncClient) -> None:
    """健康检查端点返回 ok。"""
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


async def test_list_projects_returns_200(client: AsyncClient) -> None:
    """GET /api/v1/projects/ 应返回 200 且为分页 camelCase 结构。"""
    resp = await client.get("/api/v1/projects/")
    assert resp.status_code == 200
    data = resp.json()
    # 分页契约：list / total / page / pageSize
    assert "list" in data
    assert "total" in data
    assert "page" in data
    assert "pageSize" in data


async def test_project_crud_flow(client: AsyncClient) -> None:
    """项目创建-查询-更新-删除 全流程。"""
    # 创建
    payload = {"name": "测试项目", "code": "P-001", "client": "某地产"}
    resp = await client.post("/api/v1/projects/", json=payload)
    assert resp.status_code == 201, resp.text
    created = resp.json()
    assert created["name"] == "测试项目"
    assert created["code"] == "P-001"
    assert "createdAt" in created  # camelCase 时间戳
    pid = created["id"]

    # 查询详情
    resp = await client.get(f"/api/v1/projects/{pid}")
    assert resp.status_code == 200
    assert resp.json()["id"] == pid

    # 更新（部分字段，PUT 语义但仅更新传入字段）
    resp = await client.put(f"/api/v1/projects/{pid}", json={"status": "active"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "active"
    assert resp.json()["name"] == "测试项目"  # 未传字段保持不变

    # 列表包含新项目
    resp = await client.get("/api/v1/projects/")
    assert resp.json()["total"] >= 1

    # 删除
    resp = await client.delete(f"/api/v1/projects/{pid}")
    assert resp.status_code in (200, 204)

    # 删除后查询 404
    resp = await client.get(f"/api/v1/projects/{pid}")
    assert resp.status_code == 404
