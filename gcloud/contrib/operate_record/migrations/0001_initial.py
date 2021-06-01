# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-03-01 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TaskOperateRecord",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("operator", models.CharField(max_length=128, verbose_name="操作人")),
                (
                    "operate_type",
                    models.CharField(
                        choices=[
                            ("none", "None"),
                            ("create", "创建"),
                            ("task_clone", "克隆(创建)"),
                            ("start", "执行"),
                            ("pause", "暂停"),
                            ("resume", "继续"),
                            ("revoke", "撤消"),
                            ("delete", "删除"),
                            ("update", "修改"),
                            ("retry", "重试"),
                            ("skip", "跳过"),
                            ("skip_exg", "跳过失败网关"),
                            ("pause_subproc", "暂停节点"),
                            ("resume_subproc", "继续节点"),
                            ("forced_fail", "强制失败"),
                            ("spec_nodes_timer_reset", "调整时间"),
                            ("task_action", "任务操作"),
                            ("nodes_action", "节点操作"),
                        ],
                        max_length=64,
                        verbose_name="操作类型",
                    ),
                ),
                (
                    "operate_source",
                    models.CharField(
                        choices=[
                            ("app", "app 页面"),
                            ("api", "api 接口"),
                            ("project", "项目流程"),
                            ("common", "公共流程"),
                            ("onetime", "一次性任务"),
                        ],
                        max_length=64,
                        verbose_name="操作来源",
                    ),
                ),
                ("instance_id", models.IntegerField(verbose_name="记录对象实例ID")),
                ("project_id", models.IntegerField(blank=True, default=-1, verbose_name="所属项目id")),
                ("operate_date", models.DateTimeField(auto_now_add=True, verbose_name="操作时间")),
                ("node_id", models.CharField(blank=True, default="", max_length=255, verbose_name="任务实例节点ID")),
            ],
            options={
                "verbose_name": "任务操作记录",
                "verbose_name_plural": "任务操作记录",
            },
        ),
        migrations.CreateModel(
            name="TemplateOperateRecord",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("operator", models.CharField(max_length=128, verbose_name="操作人")),
                (
                    "operate_type",
                    models.CharField(
                        choices=[
                            ("none", "None"),
                            ("create", "创建"),
                            ("task_clone", "克隆(创建)"),
                            ("start", "执行"),
                            ("pause", "暂停"),
                            ("resume", "继续"),
                            ("revoke", "撤消"),
                            ("delete", "删除"),
                            ("update", "修改"),
                            ("retry", "重试"),
                            ("skip", "跳过"),
                            ("skip_exg", "跳过失败网关"),
                            ("pause_subproc", "暂停节点"),
                            ("resume_subproc", "继续节点"),
                            ("forced_fail", "强制失败"),
                            ("spec_nodes_timer_reset", "调整时间"),
                            ("task_action", "任务操作"),
                            ("nodes_action", "节点操作"),
                        ],
                        max_length=64,
                        verbose_name="操作类型",
                    ),
                ),
                (
                    "operate_source",
                    models.CharField(
                        choices=[
                            ("app", "app 页面"),
                            ("api", "api 接口"),
                            ("project", "项目流程"),
                            ("common", "公共流程"),
                            ("onetime", "一次性任务"),
                        ],
                        max_length=64,
                        verbose_name="操作来源",
                    ),
                ),
                ("instance_id", models.IntegerField(verbose_name="记录对象实例ID")),
                ("project_id", models.IntegerField(blank=True, default=-1, verbose_name="所属项目id")),
                ("operate_date", models.DateTimeField(auto_now_add=True, verbose_name="操作时间")),
            ],
            options={
                "verbose_name": "模版操作记录",
                "verbose_name_plural": "模版操作记录",
            },
        ),
        migrations.AddIndex(
            model_name="templateoperaterecord",
            index=models.Index(fields=["instance_id"], name="operate_rec_instanc_39f580_idx"),
        ),
        migrations.AddIndex(
            model_name="taskoperaterecord",
            index=models.Index(fields=["instance_id", "node_id"], name="operate_rec_instanc_d0dfad_idx"),
        ),
    ]