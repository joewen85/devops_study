# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 10:21 AM
# @Author  : Joe
# @Site    : 
# @File    : gitlab_api.py
# @Software: PyCharm
# @function: xxxxx

import gitlab


class GitLab_ApiV4(object):
    """
    gitlab api
    """
    def __init__(self, gitlab_url, gitlab_private_token):
        self.gl = gitlab.Gitlab(gitlab_url, gitlab_private_token)
        self.gl.auth()

    def get_all_project(self):
        """
        获取所有项目列表
        :return: list
        """
        projects = self.gl.projects.list(all=True)
        # projects = self.gl.projects.get(202)
        #
        # for i in projects.members.list():
        #     print(i)

        return projects

    def get_groups(self, group_id):
        """
        获取某组
        :param group_id
        :return: group_object
        """
        group = self.gl.groups.get(group_id)
        return group

    # def get_users(self, username_id):
    #     user = self.gl.users.get(username_id)
    #     return user
    def get_users(self, username):
        """
        通过传入用户名，获取id
        :param username
        :return: user_object
        """
        users = self.gl.users.list(all=True)
        try:
            user_id = [user.id for user in users if username == user.username][0]
            user_obj = self.gl.users.get(user_id)
            return user_obj
        except:
            return None

    def get_project(self, project_id):
        """
        获取某项目
        :param project_id:
        :return:
        """
        project = self.gl.projects.get(project_id)
        return project

    def get_project_branchs(self, project_id):
        """
        获取某项目下分支
        :param project_id:
        :return: branch_list
        """
        try:
            project = self.get_project(project_id)
            branchs = project.branches.list()
            # for branch in branchs:
            #     print(branch)
        except Exception as e:
            print(e)
        return branchs

    def get_project_version(self, project_id):
        """
        获取某项目下tags列表
        :param project_id:
        :return: tags list
        """
        try:
            project = self.get_project(project_id)
            tags = project.tags.list()
        except Exception as e:
            print(e)
        return tags

    def get_project_commit(self, project_id):
        """
        获取某项目下commit log
        :param project_id:
        :return: commit_log list
        """
        try:
            project = self.get_project(project_id)
            commits = project.commits.list()
        except:
            print(Exception)
        return commits


# if __name__ == '__main__':
#     a = GitLab_ApiV4()
