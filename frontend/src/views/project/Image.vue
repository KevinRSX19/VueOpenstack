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
			</el-form>
		</el-col>

		<!--列表-->
		<el-table :data="users" highlight-current-row v-loading="loading" style="width: 100%;">
			<el-table-column type="index">
			</el-table-column>
			<el-table-column prop="name" label="名称" sortable>
			</el-table-column>
			<el-table-column prop="description" label="描述" :formatter="formatSex" sortable>
			</el-table-column>
			<el-table-column prop="container_format" label="类型" sortable>
			</el-table-column>
			<el-table-column prop="size" label="容量(byte)" sortable>
			</el-table-column>
			<el-table-column label="操作">
				<template scope="scope">
					<el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
				</template>
			</el-table-column>
		</el-table>
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
			this.$http.get('/api/image/list').then((res) => {
				console.log(res.data);
				if (res.data == 'session expire') {
					this.$router.push({ path: '/login' });
				}
				this.users = res.data.images;
				this.loading = false;
				//NProgress.done();
			}).catch(() => {
				this.$router.push({ path: '/login' });
			});
		}
	},
	handleDel: function (index, row) {
		this.$confirm('确认删除该记录吗?', '提示', {
			type: 'warning'
		}).then(() => {
			this.listLoading = true;
			//NProgress.start();
			let para = { id: row.id };
			this.$http.get('/api/image/remove_image/' + row.id).then((res) => {
				this.listLoading = false;
				//NProgress.done();
				this.$message({
					message: '删除成功',
					type: 'success'
				});
				this.getUsers();
			});
		}).catch(() => {
			this.$router.push({ path: '/login' });
		});
	},
	mounted() {
		this.getUser();
	}
};

</script>

<style scoped>

</style>