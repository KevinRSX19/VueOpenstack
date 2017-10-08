<template>
	<section>
		<!--工具条-->
		<el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
			<el-form :inline="true" :model="filters">
				<el-form-item>
					<el-input v-model="filters.name" placeholder="姓名"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" v-on:click="getUser">查询</el-button>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="handleAdd">新增</el-button>
				</el-form-item>
			</el-form>
		</el-col>
	
		<!--列表-->
		<template>
			<el-table :data="users" highlight-current-row v-loading="loading" style="width: 100%;">
				<el-table-column type="index">
				</el-table-column>
				<el-table-column prop="volume.name" label="名称" sortable>
				</el-table-column>
				<el-table-column prop="volume.description" label="描述" :formatter="formatSex" sortable>
				</el-table-column>
				<el-table-column prop="volume.format" label="类型" sortable>
				</el-table-column>
				<el-table-column prop="volume.size" label="容量(GB)" sortable>
				</el-table-column>
				<el-table-column prop="volume.status" label="状态" sortable>
				</el-table-column>
				<el-table-column prop="addr" label="操作" min-width="100" sortable>
				<template scope="scope">
					<el-button-group>
						<el-button type="primary" size="small" @click="handlePause(scope.$index, scope.row)">挂载</el-button>
						<el-button type="warning" size="small" @click="handleEdit(scope.$index, scope.row)">分离</el-button>
						<el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
					</el-button-group>
				</template>
				</el-table-column>
			</el-table>
		</template>
	
	</section>
</template>
<script>
export default {
	data() {
		return {
			filters: {
				name: ''
			},
			loading: false,
			users: [
			]
		}
	},
	methods: {
		//性别显示转换
		formatSex: function (row, column) {
			return row.sex == 1 ? '男' : row.sex == 0 ? '女' : '未知';
		},
		//获取用户列表
		getUser: function () {
			let para = {
				name: this.filters.name
			};
			this.loading = true;
			//NProgress.start();
			this.$http.get('/api/volume/list').then((res) => {
				console.log(res.data);
				if (res.data == 'session expire') {
					this.$router.push({ path: '/login' });
				}
				this.users = res.data;
				this.loading = false;
				//NProgress.done();
			}).catch(() => {
				this.$router.push({ path: '/login' });
			});
		},
		handleAdd: function() {
			console.log('volume add')
		}
	},
	mounted() {
		this.getUser();
	}
};

</script>

<style scoped>

</style>