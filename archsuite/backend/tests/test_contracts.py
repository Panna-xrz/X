"""商务管理 API 测试：合同 CRUD + 收费节点流程。"""


async def _create_project(client: AsyncClient) -> int:
    """创建测试项目并返回 ID。"""
    resp = await client.post("/api/v1/projects", json={"name": "项目A", "code": "PA"})
    assert resp.status_code == 201
    return resp.json()["id"]


async def _create_contract(client: AsyncClient, project_id: int) -> int:
    """创建测试合同并返回 ID。"""
    resp = await client.post(
        "/api/v1/contracts",
        json={"name": "设计主合同", "type": "main", "projectId": project_id, "amount": 1000000},
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["id"]


async def test_contract_crud_flow(client: AsyncClient) -> None:
    """合同创建-查询（type 别名）-更新-删除 全流程。"""
    pid = await _create_project(client)
    cid = await _create_contract(client, pid)

    # 详情：contract_type 以别别 type 输出
    resp = await client.get(f"/api/v1/contracts/{cid}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "设计主合同"
    assert data["type"] == "main"
    assert data["projectId"] == pid
    assert "createdAt" in data

    # 更新金额
    resp = await client.put(f"/api/v1/contracts/{cid}", json={"amount": 2000000})
    assert resp.status_code == 200
    assert resp.json()["amount"] == 2000000

    # 列表过滤 projectId
    resp = await client.get(f"/api/v1/contracts?projectId={pid}")
    assert resp.status_code == 200
    assert resp.json()["total"] == 1

    # 删除
    resp = await client.delete(f"/api/v1/contracts/{cid}")
    assert resp.status_code == 204
    resp = await client.get(f"/api/v1/contracts/{cid}")
    assert resp.status_code == 404


async def test_contract_node_flow(client: AsyncClient) -> None:
    """收费节点：创建-按合同查询-跨合同分页-更新-删除。"""
    pid = await _create_project(client)
    cid = await _create_contract(client, pid)

    # 创建节点
    resp = await client.post(
        "/api/v1/nodes",
        json={
            "name": "方案设计款",
            "ratio": 30,
            "amount": 300000,
            "planDate": "2026-01-15",
            "status": "planned",
            "contractId": cid,
        },
    )
    assert resp.status_code == 201, resp.text
    node = resp.json()
    assert node["name"] == "方案设计款"
    assert node["contractId"] == cid
    nid = node["id"]

    # 按合同查询（节点路由）
    resp = await client.get(f"/api/v1/contracts/{cid}/nodes")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    # 跨合同分页查询（contractId 过滤）
    resp = await client.get(f"/api/v1/nodes?contractId={cid}&page=1&pageSize=10")
    assert resp.status_code == 200
    assert resp.json()["total"] == 1

    # 更新状态为已收款
    resp = await client.put(f"/api/v1/nodes/{nid}", json={"status": "received"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "received"

    # 删除
    resp = await client.delete(f"/api/v1/nodes/{nid}")
    assert resp.status_code == 204


async def test_node_create_with_missing_contract_404(client: AsyncClient) -> None:
    """为不存在的合同创建节点应返回 404。"""
    resp = await client.post(
        "/api/v1/nodes",
        json={"name": "无效节点", "contractId": 99999},
    )
    assert resp.status_code == 404
