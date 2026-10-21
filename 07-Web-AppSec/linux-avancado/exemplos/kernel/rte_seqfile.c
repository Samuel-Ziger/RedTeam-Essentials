// SPDX-License-Identifier: GPL-2.0
#include <linux/init.h>
#include <linux/module.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>

#define RTE_ENTRY "rte_advanced"

static int rte_show(struct seq_file *stream, void *unused)
{
    (void)unused;
    seq_puts(stream, "schema=rte-kernel-module/v1\n");
    seq_puts(stream, "purpose=seq_file_lifecycle_demo\n");
    return 0;
}

static int rte_open(struct inode *inode, struct file *file)
{
    (void)inode;
    return single_open(file, rte_show, NULL);
}

static const struct proc_ops rte_ops = {
    .proc_open = rte_open,
    .proc_read = seq_read,
    .proc_lseek = seq_lseek,
    .proc_release = single_release,
};

static int __init rte_init(void)
{
    if (proc_create(RTE_ENTRY, 0444, NULL, &rte_ops) == NULL)
        return -ENOMEM;
    pr_info("rte_seqfile: loaded\n");
    return 0;
}

static void __exit rte_exit(void)
{
    remove_proc_entry(RTE_ENTRY, NULL);
    pr_info("rte_seqfile: unloaded\n");
}

module_init(rte_init);
module_exit(rte_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("RedTeam Essentials course");
MODULE_DESCRIPTION("Safe seq_file lifecycle demonstration");
