module.exports = {
    getUser: (req, res, next) => {
        req.app.get('db').read.user_by_id([req.user.id]).then((user) => {
            return res.status(200).json(user[0]);
        });
    },

    getKatasByKataId: (req, res, next) => {
        req.app.get('db').read.kata_by_id([req.params.kataid]).then((kata) => {
            return res.status(200).json(kata[0]);
        })
    },

    getRandomKata: (req, res, next) => {
        let kataLevel = parseInt(req.params.userkyu);
        let bottomRange = kataLevel - 1;
        let topRange = kataLevel + 1;
        req.app.get('db').read.random_kata([bottomRange, topRange]).then((katas) => {
            return res.status(200).json(katas[Math.floor(Math.random() * katas.length)]);
        })
    },

    getRandomKataList: (req, res, next) => {
        req.app.get('db').read.random_kata_list().then((katas) => {
            return res.status(200).json(katas);
        })
    },

    getKatasByKyu: (req, res, next) => {
        req.app.get('db').read.katas_by_kyu([req.params.kyu]).then((katas) => {
            return res.status(200).json(katas);
        })
    },

    getKataSolutions: (req, res, next) => {
        req.app.get('db').read.kata_solutions([req.params.kataid]).then((solutions) => {
            return res.status(200).json(solutions);
        })
    },

    getUserKatas: (req, res, next) => {
        req.app.get('db').read.user_katas([req.params.userid]).then((katas) => {
            return res.status(200).json(katas);
        })
    },

    searchByKatasName: (req, res, next) => {
        req.app.get('db').read.by_kata_name([req.body.userInput]).then((katas) => {
            if (err) return next(err);
            return res.status(200).json(katas);
        })
    },

    sumbitAnswer: (req, res, next) => {
        req.app.get('db').create.solution([req.body.userid, req.params.kataid, req.body.script]).then((solution) => {
            return res.status(201).json(solution);
        })
    },

    getKataVotes: (req, res, next) => {
        req.app.get('db').read.all_kata_likes([]).then((likes) => {
            req.app.get('db').read.all_kata_dislikes([]).then((dislikes) => {
                req.app.get('db').read.all_kata_votes([]).then((votes) => {
                    return res.status(200).json([likes, dislikes, votes]);
                })
            })
        })
    },

    getSolutionVotes: (req, res, next) => {
        req.app.get('db').read.all_solution_likes([]).then((likes) => {
            req.app.get('db').read.all_solution_dislikes([]).then((err, dislikes) => {
                req.app.get('db').read.all_solution_votes([]).then((err, votes) => {
                    return res.status(200).json([likes, dislikes, votes]);
                })
            })
        })
    },

    voteKata: (req, res, next) => {
        req.app.get('db').read.check_kata_vote([req.body.userid, req.body.kataid]).then((data) => {
            if (data.length === 0) {
                req.app.get('db').create.kata_likes([req.body.userid, req.body.kataid, req.body.vote], (err, change) => {
                    if (err) return next(err);
                    req.app.get('db').read.get_kata_likes([req.body.kataid], (err, likes) => {
                        if (err) return next(err);
                        req.app.get('db').read.get_kata_dislikes([req.body.kataid], (err, dislikes) => {
                            if (err) return next(err);
                            req.app.get('db').read.get_kata_votes([req.body.kataid], (err, votes) => {
                                if (err) return next(err);
                                return res.status(200).json({likes: likes[0].likes, dislikes: dislikes[0].dislikes, votes: votes[0].votes});
                            })
                        })
                    })
                })
            } else {
                req.app.get('db').update.change_kata_vote([req.body.userid, req.body.kataid, req.body.vote], (err, rating) => {
                    if (err) return next(err);
                    req.app.get('db').read.get_kata_likes([req.body.kataid], (err, likes) => {
                        if (err) return next(err);
                        req.app.get('db').read.get_kata_dislikes([req.body.kataid], (err, dislikes) => {
                            if (err) return next(err);
                            req.app.get('db').read.get_kata_votes([req.body.kataid], (err, votes) => {
                                if (err) return next(err);
                                return res.status(200).json({likes: likes[0].likes, dislikes: dislikes[0].dislikes, votes: votes[0].votes});
                            })
                        })
                    })
                })
            }
        })

    },

    voteSolution: (req, res, next) => {
        req.app.get('db').read.check_solution_vote([req.body.userid, req.body.solutionid], (err, data) => {
            if (err) return next(err);
            if (data.length === 0) {
                req.app.get('db').create.solution_likes([req.body.userid, req.body.solutionid, req.body.vote], (err, change) => {
                    if (err) return next(err);
                    req.app.get('db').read.get_solution_likes([req.body.solutionid], (err, likes) => {
                        if (err) return next(err);
                        req.app.get('db').read.get_solution_dislikes([req.body.solutionid], (err, dislikes) => {
                            if (err) return next(err);
                            req.app.get('db').read.get_solution_votes([req.body.solutionid], (err, votes) => {
                                if (err) return next(err);
                                return res.status(200).json({likes: likes[0].likes, dislikes: dislikes[0].dislikes, votes: votes[0].votes});
                            })
                        })
                    })
                })
            } else {
                req.app.get('db').update.change_solution_vote([req.body.userid, req.body.solutionid, req.body.vote], (err, rating) => {
                    if (err) return next(err);
                    req.app.get('db').read.get_solution_likes([req.body.solutionid], (err, likes) => {
                        if (err) return next(err);
                        req.app.get('db').read.get_solution_dislikes([req.body.solutionid], (err, dislikes) => {
                            if (err) return next(err);
                            req.app.get('db').read.get_solution_votes([req.body.solutionid], (err, votes) => {
                                if (err) return next(err);
                                return res.status(200).json({likes: likes[0].likes, dislikes: dislikes[0].dislikes, votes: votes[0].votes});
                            })
                        })
                    })
                })
            }
        })

    },

    addPointsToUser: (req, res, next) => {
        req.app.get('db').update.user_points([req.body.points, req.user.id], (err) => {
            if (err) return next(err);
            return res.sendStatus(200)
        })
    },

    checkAuth: (req, res, next) => {
        if (req.isAuthenticated()) {
            res.sendStatus(200);
        } else {
            res.sendStatus(401);
        }
    }

};
