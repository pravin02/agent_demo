import sqlite3
from dataclasses import dataclass

from pydantic import BaseModel

from pydantic_ai import Agent, RunContext

from pydantic_ai.models.ollama import OllamaModel

from pydantic_ai.providers.ollama import OllamaProvider

import os
from dotenv import load_dotenv


@dataclass
class DatabaseConn:
    """A wrapper over the SQLite connection."""

    sqlite_conn: sqlite3.Connection

    async def customer_name(self, *, id: int) -> str | None:
        res = cur.execute("SELECT name FROM customers WHERE id=?", (id,))
        row = res.fetchone()
        if row:
            return row[0]
        return None

    async def customer_balance(self, *, id: int) -> float:
        res = cur.execute("SELECT balance FROM customers WHERE id=?", (id,))
        row = res.fetchone()
        if row:
            return row[0]
        else:
            raise ValueError("Customer not found")


@dataclass
class SupportDependencies:
    customer_id: int
    db: DatabaseConn


class SupportOutput(BaseModel):
    support_advice: str
    """Advice returned to the customer"""
    block_card: bool
    """Whether to block their card or not"""
    risk: int
    """Risk level of query"""


load_dotenv()

model_name = os.getenv("MODEL_NAME") or ""
base_url = os.getenv("OLLAMA_BASE_URL")

model = OllamaModel(model_name, provider=OllamaProvider(base_url))

support_agent = Agent(
    model,
    deps_type=SupportDependencies,
    output_type=SupportOutput,
    instructions=(
        "You are a support agent in our bank, give the "
        "customer support and judge the risk level of their query. "
        "Reply using the customer's name."
    ),
)


@support_agent.instructions
async def add_customer_name(ctx: RunContext[SupportDependencies]) -> str:
    customer_name = await ctx.deps.db.customer_name(id=ctx.deps.customer_id)
    return f"The customer's name is {customer_name!r}"


@support_agent.tool
async def customer_balance(ctx: RunContext[SupportDependencies]) -> str:
    """Returns the customer's current account balance."""
    balance = await ctx.deps.db.customer_balance(
        id=ctx.deps.customer_id,
    )
    return f"${balance:.2f}"


if __name__ == "__main__":
    with sqlite3.connect(":memory:") as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE customers(id, name, balance)")
        cur.execute(
            """
            INSERT INTO customers VALUES
                (123, 'John', 123.45)
        """
        )
        con.commit()

        deps = SupportDependencies(customer_id=123, db=DatabaseConn(sqlite_conn=con))

        while True:
            query = input("User: ")
            if query == "quit" or query == "exit":
                print("User choose to exit")
                break
            result = support_agent.run_sync(query, deps=deps)
            print(result.output)
