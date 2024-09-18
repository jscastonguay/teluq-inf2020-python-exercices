# Nom de l'exécutable
EXEC = encrypteur

# Compilateur
CC = gcc

# Options de compilation
CFLAGS = -Wall -Wextra -g

# Fichiers sources
SRCS = main.c

# Fichiers objets
OBJS = $(SRCS:.c=.o)

# Règle par défaut, créer l'exécutable
all: $(EXEC)

# Créer l'exécutable en liant les fichiers objets
$(EXEC): $(OBJS)
	$(CC) $(CFLAGS) -o $(EXEC) $(OBJS)

# Règle pour compiler les fichiers .c en .o
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
	

# Nettoyer les fichiers objets et l'exécutable
clean:
	rm -f $(OBJS) $(EXEC)

# Nettoyer complètement, y compris les fichiers de sauvegarde
mrproper: clean
	rm -f *~ 

# Règle de phonie (pour ne pas chercher de fichier nommé "clean" ou "all")
.PHONY: all clean mrproper