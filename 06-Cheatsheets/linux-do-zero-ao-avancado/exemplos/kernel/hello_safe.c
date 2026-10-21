// SPDX-License-Identifier: GPL-2.0-only
#include <linux/init.h>
#include <linux/module.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("RedTeam Essentials - curso Linux");
MODULE_DESCRIPTION("Modulo didatico que apenas registra carga e descarga");
MODULE_VERSION("1.0");

static int __init hello_safe_init(void)
{
	pr_info("hello_safe: modulo didatico carregado\n");
	return 0;
}

static void __exit hello_safe_exit(void)
{
	pr_info("hello_safe: modulo didatico removido\n");
}

module_init(hello_safe_init);
module_exit(hello_safe_exit);
