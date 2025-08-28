from typing import List

class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:

        res = []
        for i in range(len(nums)):
            ans = nums[i] * nums[i]
            res.append(ans)


        return sorted(res)




if __name__ == "__main__":
    sol = Solution()
    print(sol.sortedSquares([-4,-1,0,3,10]))