def dish_delete_use_case(repo, id: int):
    return repo.delete(id)