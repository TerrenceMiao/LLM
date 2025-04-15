package org.paradise.mcp

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class McpApplication

fun main(args: Array<String>) {
	runApplication<McpApplication>(*args)
}
