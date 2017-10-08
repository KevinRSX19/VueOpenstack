<template>
    <section class="chart-container">
        <el-row>
            <el-col class="border" :span="7">
                <el-card :body-style="{ padding: '0px' }">
                    <div class="card">
                        <el-col>
                            <div class="hp">
                                <div class="title">健康指数</div>
                            </div>
                            <hr style="height: 1px; border:none; border-top:1px solid #CCCCCC;" />
                        </el-col>
                        <el-col :span="14" class="center">
                            <img src="../../assets/健康大.png">
                        </el-col>
                        <el-col :span="10" style="height:80%;">
                            <el-col style="height:33%;">
                                <img class="points" src="../../assets/健康小.png">
                            </el-col>
                            <el-col style="height:33%;">
                                <img class="points" src="../../assets/危险小.png">
                            </el-col>
                            <el-col style="height:33%;">
                                <img class="points" src="../../assets/严重小.png">
                            </el-col>
                        </el-col>
                    </div>
                </el-card>
            </el-col>
            <el-col class="border" :span="8">
                <el-card :body-style="{ padding: '0px' }">
                    <div class="card">
                        <div class="ei">
                                <div class="title">异常信息</div>
                            </div>
                        <hr style="height: 1px; border:none; border-top:1px solid #CCCCCC;" />
                        <el-row>
                            <el-col :span="12" :offset="2">
                                <span style="font-size:35px; font-weight:bold; color:#F00;">{{err_no}}</span>个异常
                            </el-col>
                            <el-col :span="10">
                                <el-col><img src="../../assets/危险数.png">危险数</el-col>
                                <el-col><img src="../../assets/严重数.png">严重数</el-col>
                            </el-col>
                        </el-row>
                        <hr style="height: 1px; border:none; border-top:1px solid #CCCCCC;" />
                        <el-row>
                            <el-col :span="8">虚拟机异常</el-col>
                            <el-col :span="8">{{vmer_no}}</el-col>
                            <el-col :span="4"><img src="../../assets/危险数.png">{{vmer_no_d}}</el-col>
                            <el-col :span="4"><img src="../../assets/严重数.png">{{vmer_no_s}}</el-col>
                        </el-row>
                        <hr style="height: 1px; border:none; border-top:1px solid #CCCCCC;" />
                        <el-row>
                            <el-col :span="8">主机异常</el-col>
                            <el-col :span="8">{{hoster_no}}</el-col>
                            <el-col :span="4"><img src="../../assets/危险数.png">{{hoster_no_d}}</el-col>
                            <el-col :span="4"><img src="../../assets/严重数.png">{{hoster_no_s}}</el-col>
                        </el-row>
                        <hr style="height: 1px; border:none; border-top:1px solid #CCCCCC;" />
                        <el-row>
                            <el-col :span="8">磁盘异常</el-col>
                            <el-col :span="8">{{voler_no}}</el-col>
                            <el-col :span="4"><img src="../../assets/危险数.png">{{voler_no_d}}</el-col>
                            <el-col :span="4"><img src="../../assets/严重数.png">{{voler_no_s}}</el-col>
                        </el-row>
                    </div>
                </el-card>
            </el-col>
            <el-col class="border" :span="8">
                <el-card :body-style="{ padding: '0px' }">
                    <div class="card">
                        <div class="wl">
                                <div class="title">警告日志TOP5</div>
                            </div>
                        <div class="bottom clearfix">
                            <hr style="height: 1px; border:none; border-top:1px solid #CCCCCC;" />
                            <el-table class="table" :data="warlog" :show-header="false" v-loading="loading" style="width: 100%;">
                                <el-table-column min-width="130" label="名称">
                                    <template scope="scope">
                                        <span style="height=28px;color:#F00;font-size:12px;">{{ scope.row.name }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column prop="date" label="日期">
                                                        </el-table-column>
                                <el-table-column prop="time" label="时间">
                                </el-table-column>
                            </el-table>
                        </div>
                    </div>
                </el-card>
            </el-col>
        </el-row>
        <el-row>
            <el-col class="border" :span="5">
                <el-card :body-style="{ padding: '0px' }">
                    <div class="card" style="padding: 14px;">
                        <div class="cpu1">
                                <div class="title">CPU占用率</div>
                            </div>
                        <hr style="height: 1px; border:none; border-top:1px solid #CCCCCC;" />
                        <el-col class="center">
                            <svg width="200" height="180"></svg>
                        </el-col>
                    </div>
                </el-card>
            </el-col>
            <el-col class="border" :span="8">
                <el-card :body-style="{ padding: '0px' }">
                    <div class="card" style="padding: 14px;">
                        <div class="title2" style="padding-bottom:10px">CPU占用率</div>
                        <hr style="height: 1px; border:none; border-top:1px solid #CCCCCC;" />
                        <el-col class="center" style="padding-top:0px">
                            <svg width="200" height="180"></svg>
                        </el-col>
                    </div>
                </el-card>
            </el-col>
            <el-col class="border" :span="10">
                <el-card :body-style="{ padding: '0px' }">
                    <div class="card" style="padding: 14px;">
                        <el-col :span="8">
                        <div class="title2">存储状态</div>
                            <div class="bottom clearfix">
                                <svg class="a" width="100" height="100"></svg>
                            </div>
                        </el-col>
                        <el-col :span="8">
                        <div class="title2">虚拟机状态</div>
                            <div class="bottom clearfix">
                            <div class="bottom clearfix">
                                <svg class="a" width="100" height="100"></svg>
                            </div>
                            </div>
                        </el-col>
                        <el-col :span="8">
                        <div class="title2">主机状态</div>
                            <div class="bottom clearfix">
                            <div class="bottom clearfix">
                                <svg class="a" width="100" height="100"></svg>
                            </div>
                            </div>
                        </el-col>
                    </div>
                </el-card>
            </el-col>
        </el-row>
        <el-row>
            <el-col class="border" :span="5">
                <el-card :body-style="{ padding: '0px' }">
                    <div class="card" style="padding: 14px;">
                        <div class="mem">
                                <div class="title">内存占用率</div>
                            </div>
                        <hr style="height: 1px; border:none; border-top:1px solid #CCCCCC;" />
                        <el-col class="center">
                            <svg width="200" height="180"></svg>
                        </el-col>
                    </div>
                </el-card>
            </el-col>
            <el-col class="border" :span="8">
                <el-card :body-style="{ padding: '0px' }">
                    <div class="card" style="padding: 14px;">
                        <div class="title2" style="padding-bottom:10px">内存占用率</div>
                        <hr style="height: 1px; border:none; border-top:1px solid #CCCCCC;" />
                        <el-col class="center" style="padding-top:0px">
                            <svg width="200" height="180"></svg>
                        </el-col>
                    </div>
                </el-card>
            </el-col>
            <el-col class="border" :span="10">
                <el-card :body-style="{ padding: '0px' }">
                    <div class="card" style="padding: 14px;">
                        <div class="ol">
                                <div class="title">操作事件TOP5</div>
                            </div>
                        <div class="bottom clearfix">
                            <hr style="height: 1px; border:none; border-top:1px solid #CCCCCC;" />
                            <el-table :data="actlog" :show-header="false" v-loading="loading" style="width: 100%;">
                                <el-table-column min-width="130" prop="name" label="操作">
                                </el-table-column>
                                <el-table-column prop="user" label="用户">
                                </el-table-column>
                                <el-table-column prop="date" label="日期">
                                </el-table-column>
                                <el-table-column prop="time" label="时间">
                                </el-table-column>
                            </el-table>
                        </div>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </section>
</template>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script>
const d3 = require('d3');

export default {
    data() {
        return {
            filters: {
                name: ''
            },
            loading: false,
            users: [{
                id: '12987122',
                name: '好滋好味鸡蛋仔',
                category: '江浙小吃、小吃零食',
                desc: '荷兰优质淡奶，奶香浓而不腻',
                address: '上海市普陀区真北路',
                shop: '王小虎夫妻店',
                shopId: '10333'
            }
            ],

            chartColumn: null,

            err_no: '10',
            vmer_no: '3',
            vmer_no_d: '1',
            vmer_no_s: '2',
            hoster_no: '0',
            hoster_no_d: '0',
            hoster_no_s: '0',
            voler_no: '0',
            voler_no_d: '0',
            voler_no_s: '0',
            warlog: [{
                date: '2017.4.8',
                name: 'CPU占用率100%',
                time: '14:55'
            }, {
                date: '2017.4.8',
                name: '主机无法连接',
                time: '14:55'
            }, {
                date: '2017.4.8',
                name: '内存占用率80%',
                time: '14:55'
            }, {
                date: '2017.4.8',
                name: '异常用户登陆',
                time: '14:55'
            }, {
                date: '2017.4.8',
                name: '磁盘空间不足',
                time: '14:55'
            },],
            actlog: [{
                date: '2017.4.8',
                name: '创建虚拟机',
                user: 'admin',
                time: '14:55'
            }, {
                date: '2017.4.8',
                name: '创建网络',
                user: 'admin',
                time: '14:55'
            }, {
                date: '2017.4.8',
                name: '扩展主机',
                user: 'admin',
                time: '14:55'
            }, {
                date: '2017.4.8',
                name: '下载系统日志',
                user: 'admin',
                time: '14:55'
            }, {
                date: '2017.4.8',
                name: '删除虚拟机',
                user: 'admin',
                time: '14:55'
            },],
        }
    },
    methods: {
        
    },
    mounted: function() {
        d3.selectAll('svg')
      .append('circle')
      .attr('cx', '100')
      .attr('cy', '100')
      .attr('r', '60')
    },
    updated: function() {
    }
}
</script>

<style scoped>
div.el-col.border {
    margin: 5px;
}

div.el-col.center {
    text-align: center;
    padding: 5% 0 0 0;
}

.el-table {
    border: 0px;
}

.el-table td {
    height: 28px;
}

.el-table::after {
    background-color: #fbfdff;
}

.chart-container {
    width: 100%;
    float: left;
}

span.title {
    padding-top: 10px;
    padding-bottom: 10px;
    line-height: 28px;
    height: 14px;
}

div.card {
    padding: 10px;
    height: 240px;
}

div.title {
    padding-top: 10px;
    padding-left:27px;
    font-size:16px;
    color: #6584aa;
}

div.title2 {
    padding-top: 10px;
    padding-left:10px;
    font-size:16px;
    color: #6584aa;
}

div.hp {
    padding-bottom: 10px;
    background:url(../../assets/健康指数.png) no-repeat left center; 
}

div.ei {
    padding-bottom: 10px;
    background:url(../../assets/异常信息.png) no-repeat left center; 
}

div.wl {
    padding-bottom: 10px;
    background:url(../../assets/告警日志.png) no-repeat left center; 
}

div.cpu1 {
    padding-bottom: 10px;
    background:url(../../assets/CPU占用率.png) no-repeat left center; 
}

div.mem {
    padding-bottom: 10px;
    background:url(../../assets/内存占用率.png) no-repeat left center; 
}

div.ol {
    padding-bottom: 10px;
    background:url(../../assets/操作事件.png) no-repeat left center; 
}

svg.a {
    padding-top: 50px;
}

img.points {
    padding-top: 10px;
    padding-bottom: 10px;
}

.progress-meter .background {
    fill: #ccc;
}

.progress-meter .foreground {
    fill: #000;
}

.progress-meter text {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 24px;
    font-weight: bold;
}
</style>
