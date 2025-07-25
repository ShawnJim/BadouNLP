# -*- coding: utf-8 -*-
import torch
from loader import load_data
import time

"""
模型效果测试
"""


class Evaluator:
    def __init__(self, config, model, logger):
        self.config = config
        self.model = model
        self.logger = logger
        self.valid_data = load_data(config["valid_data_path"], config, shuffle=False)
        self.stats_dict = {"correct": 0, "wrong": 0}  # 用于存储测试结果

    def eval(self, epoch):
        # self.logger.info(f"开始测试第{epoch}轮模型效果：")
        self.model.eval()
        self.stats_dict = {"correct": 0, "wrong": 0}  # 清空上一轮结果
        start = time.perf_counter()     # 统计预测时间
        for index, batch_data in enumerate(self.valid_data):
            if torch.cuda.is_available():
                batch_data = [d.cuda() for d in batch_data]
            input_ids, labels = batch_data  # 输入变化时这里需要修改，比如多输入，多输出的情况
            with torch.no_grad():
                pred_results = self.model(input_ids)  # 不输入labels，使用模型当前参数进行预测
            self.write_stats(labels, pred_results)
        acc = self.show_stats()
        elapsed = time.perf_counter() - start   # 统计预测时间
        return acc, elapsed

    def write_stats(self, labels, pred_results):
        assert len(labels) == len(pred_results)
        for true_label, pred_label in zip(labels, pred_results):
            pred_label = torch.argmax(pred_label)
            if int(true_label) == int(pred_label):
                self.stats_dict["correct"] += 1
            else:
                self.stats_dict["wrong"] += 1
        return

    def show_stats(self):
        correct = self.stats_dict["correct"]
        wrong = self.stats_dict["wrong"]
        # self.logger.info(f"预测集合条目总量：{correct + wrong}")
        # self.logger.info(f"预测正确条目：{correct}，预测错误条目：{wrong}")
        # self.logger.info(f"预测准确率：{(correct / (correct + wrong)):.4f}")
        # self.logger.info("--------------------")
        return correct / (correct + wrong)
