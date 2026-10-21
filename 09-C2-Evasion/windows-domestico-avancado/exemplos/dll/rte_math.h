#ifndef RTE_MATH_H
#define RTE_MATH_H

#ifdef RTE_MATH_EXPORTS
#define RTE_API __declspec(dllexport)
#else
#define RTE_API __declspec(dllimport)
#endif

RTE_API int rte_add(int left, int right);
RTE_API unsigned int rte_api_version(void);

#endif

