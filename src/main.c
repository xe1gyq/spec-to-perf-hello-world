#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* Volatile reads keep every traversal observable to the compiler. This is a
 * controlled memory-access lesson, not a production matrix implementation. */
__attribute__((noinline))
uint64_t sum_rows(const volatile uint32_t *data, size_t n) {
    uint64_t sum = 0;
    for (size_t row = 0; row < n; ++row)
        for (size_t col = 0; col < n; ++col)
            sum += data[row * n + col];
    return sum;
}

__attribute__((noinline))
uint64_t sum_columns(const volatile uint32_t *data, size_t n) {
    uint64_t sum = 0;
    for (size_t col = 0; col < n; ++col)
        for (size_t row = 0; row < n; ++row)
            sum += data[row * n + col];
    return sum;
}

static int parse(const char *s, size_t limit, size_t *out) {
    if (!*s) return 0;
    for (const char *p = s; *p; ++p)
        if (*p < '0' || *p > '9') return 0;
    errno = 0;
    char *end;
    unsigned long long value = strtoull(s, &end, 10);
    if (errno || *end || value == 0 || value > limit) return 0;
    *out = (size_t)value;
    return 1;
}

static double seconds(struct timespec t) {
    return (double)t.tv_sec + (double)t.tv_nsec / 1e9;
}

int main(int argc, char **argv) {
    size_t n = 2048, repeats = 20;
    if (argc == 2 && strcmp(argv[1], "--help") == 0) {
        puts("Usage: matrix-scan {row|column} [size:1..4096] [repeats:1..1000]");
        return 0;
    }
    if (argc < 2 || argc > 4 ||
        (strcmp(argv[1], "row") && strcmp(argv[1], "column")) ||
        (argc >= 3 && !parse(argv[2], 4096, &n)) ||
        (argc == 4 && !parse(argv[3], 1000, &repeats))) {
        fputs("Invalid arguments. Run matrix-scan --help.\n", stderr);
        return 2;
    }
    uint32_t *data = malloc(n * n * sizeof(*data));
    if (!data) { fputs("Allocation failed.\n", stderr); return 1; }
    uint64_t expected = 0, checksum = 0;
    for (size_t i = 0; i < n * n; ++i) {
        data[i] = (uint32_t)(i % 251);
        expected += data[i];
    }
    uint64_t (*scan)(const volatile uint32_t *, size_t) =
        strcmp(argv[1], "row") == 0 ? sum_rows : sum_columns;
    struct timespec start, end;
    if (clock_gettime(CLOCK_MONOTONIC, &start)) { free(data); return 1; }
    for (size_t r = 0; r < repeats; ++r) checksum += scan(data, n);
    if (clock_gettime(CLOCK_MONOTONIC, &end)) { free(data); return 1; }
    free(data);
    if (checksum != expected * repeats) {
        fputs("Checksum mismatch.\n", stderr); return 1;
    }
    printf("mode=%s size=%zu repeats=%zu checksum=%" PRIu64 " elapsed_seconds=%.6f\n",
           argv[1], n, repeats, checksum, seconds(end) - seconds(start));
    return 0;
}
