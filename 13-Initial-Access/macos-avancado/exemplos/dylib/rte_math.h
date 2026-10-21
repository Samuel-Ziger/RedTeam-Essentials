#ifndef RTE_MATH_H
#define RTE_MATH_H

#define RTE_API __attribute__((visibility("default")))

RTE_API int rte_add(int left, int right);
RTE_API unsigned int rte_api_version(void);

#endif
