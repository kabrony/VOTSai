# classifier

## Classes

### IntentClassifier

#### Methods

##### __init__

```python
__init__(self)
```

##### predict

```python
predict(self, query: str)
```

### MultinomialNB

Naive Bayes classifier for multinomial models.

    The multinomial Naive Bayes classifier is suitable for classification with
    discrete features (e.g., word counts for text classification). The
    multinomial distribution normally requires integer feature counts. However,
    in practice, fractional counts such as tf-idf may also work.

    Read more in the :ref:`User Guide <multinomial_naive_bayes>`.

    Parameters
    ----------
    alpha : float or array-like of shape (n_features,), default=1.0
        Additive (Laplace/Lidstone) smoothing parameter
        (set alpha=0 and force_alpha=True, for no smoothing).

    force_alpha : bool, default=True
        If False and alpha is less than 1e-10, it will set alpha to
        1e-10. If True, alpha will remain unchanged. This may cause
        numerical errors if alpha is too close to 0.

        .. versionadded:: 1.2
        .. versionchanged:: 1.4
           The default value of `force_alpha` changed to `True`.

    fit_prior : bool, default=True
        Whether to learn class prior probabilities or not.
        If false, a uniform prior will be used.

    class_prior : array-like of shape (n_classes,), default=None
        Prior probabilities of the classes. If specified, the priors are not
        adjusted according to the data.

    Attributes
    ----------
    class_count_ : ndarray of shape (n_classes,)
        Number of samples encountered for each class during fitting. This
        value is weighted by the sample weight when provided.

    class_log_prior_ : ndarray of shape (n_classes,)
        Smoothed empirical log probability for each class.

    classes_ : ndarray of shape (n_classes,)
        Class labels known to the classifier

    feature_count_ : ndarray of shape (n_classes, n_features)
        Number of samples encountered for each (class, feature)
        during fitting. This value is weighted by the sample weight when
        provided.

    feature_log_prob_ : ndarray of shape (n_classes, n_features)
        Empirical log probability of features
        given a class, ``P(x_i|y)``.

    n_features_in_ : int
        Number of features seen during :term:`fit`.

        .. versionadded:: 0.24

    feature_names_in_ : ndarray of shape (`n_features_in_`,)
        Names of features seen during :term:`fit`. Defined only when `X`
        has feature names that are all strings.

        .. versionadded:: 1.0

    See Also
    --------
    BernoulliNB : Naive Bayes classifier for multivariate Bernoulli models.
    CategoricalNB : Naive Bayes classifier for categorical features.
    ComplementNB : Complement Naive Bayes classifier.
    GaussianNB : Gaussian Naive Bayes.

    References
    ----------
    C.D. Manning, P. Raghavan and H. Schuetze (2008). Introduction to
    Information Retrieval. Cambridge University Press, pp. 234-265.
    https://nlp.stanford.edu/IR-book/html/htmledition/naive-bayes-text-classification-1.html

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.RandomState(1)
    >>> X = rng.randint(5, size=(6, 100))
    >>> y = np.array([1, 2, 3, 4, 5, 6])
    >>> from sklearn.naive_bayes import MultinomialNB
    >>> clf = MultinomialNB()
    >>> clf.fit(X, y)
    MultinomialNB()
    >>> print(clf.predict(X[2:3]))
    [3]

#### Methods

##### __init__

```python
__init__(self, alpha=1.0, force_alpha=True, fit_prior=True, class_prior=None)
```

##### fit

```python
fit(self, X, y, sample_weight=None)
```

Fit Naive Bayes classifier according to X, y.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Training vectors, where `n_samples` is the number of samples and
            `n_features` is the number of features.

        y : array-like of shape (n_samples,)
            Target values.

        sample_weight : array-like of shape (n_samples,), default=None
            Weights applied to individual samples (1. for unweighted).

        Returns
        -------
        self : object
            Returns the instance itself.

##### get_metadata_routing

```python
get_metadata_routing(self)
```

Get metadata routing of this object.

        Please check :ref:`User Guide <metadata_routing>` on how the routing
        mechanism works.

        Returns
        -------
        routing : MetadataRequest
            A :class:`~sklearn.utils.metadata_routing.MetadataRequest` encapsulating
            routing information.

##### get_params

```python
get_params(self, deep=True)
```

Get parameters for this estimator.

        Parameters
        ----------
        deep : bool, default=True
            If True, will return the parameters for this estimator and
            contained subobjects that are estimators.

        Returns
        -------
        params : dict
            Parameter names mapped to their values.

##### partial_fit

```python
partial_fit(self, X, y, classes=None, sample_weight=None)
```

Incremental fit on a batch of samples.

        This method is expected to be called several times consecutively
        on different chunks of a dataset so as to implement out-of-core
        or online learning.

        This is especially useful when the whole dataset is too big to fit in
        memory at once.

        This method has some performance overhead hence it is better to call
        partial_fit on chunks of data that are as large as possible
        (as long as fitting in the memory budget) to hide the overhead.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Training vectors, where `n_samples` is the number of samples and
            `n_features` is the number of features.

        y : array-like of shape (n_samples,)
            Target values.

        classes : array-like of shape (n_classes,), default=None
            List of all the classes that can possibly appear in the y vector.

            Must be provided at the first call to partial_fit, can be omitted
            in subsequent calls.

        sample_weight : array-like of shape (n_samples,), default=None
            Weights applied to individual samples (1. for unweighted).

        Returns
        -------
        self : object
            Returns the instance itself.

##### predict

```python
predict(self, X)
```

Perform classification on an array of test vectors X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        C : ndarray of shape (n_samples,)
            Predicted target values for X.

##### predict_joint_log_proba

```python
predict_joint_log_proba(self, X)
```

Return joint log probability estimates for the test vector X.

        For each row x of X and class y, the joint log probability is given by
        ``log P(x, y) = log P(y) + log P(x|y),``
        where ``log P(y)`` is the class prior probability and ``log P(x|y)`` is
        the class-conditional probability.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        C : ndarray of shape (n_samples, n_classes)
            Returns the joint log-probability of the samples for each class in
            the model. The columns correspond to the classes in sorted
            order, as they appear in the attribute :term:`classes_`.

##### predict_log_proba

```python
predict_log_proba(self, X)
```

Return log-probability estimates for the test vector X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        C : array-like of shape (n_samples, n_classes)
            Returns the log-probability of the samples for each class in
            the model. The columns correspond to the classes in sorted
            order, as they appear in the attribute :term:`classes_`.

##### predict_proba

```python
predict_proba(self, X)
```

Return probability estimates for the test vector X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        C : array-like of shape (n_samples, n_classes)
            Returns the probability of the samples for each class in
            the model. The columns correspond to the classes in sorted
            order, as they appear in the attribute :term:`classes_`.

##### score

```python
score(self, X, y, sample_weight=None)
```

Return the mean accuracy on the given test data and labels.

        In multi-label classification, this is the subset accuracy
        which is a harsh metric since you require for each sample that
        each label set be correctly predicted.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Test samples.

        y : array-like of shape (n_samples,) or (n_samples, n_outputs)
            True labels for `X`.

        sample_weight : array-like of shape (n_samples,), default=None
            Sample weights.

        Returns
        -------
        score : float
            Mean accuracy of ``self.predict(X)`` w.r.t. `y`.

##### set_fit_request

```python
set_fit_request(self: sklearn.naive_bayes.MultinomialNB, sample_weight: Union[bool, NoneType, str] = '$UNCHANGED$')
```

Request metadata passed to the ``fit`` method.

        Note that this method is only relevant if
        ``enable_metadata_routing=True`` (see :func:`sklearn.set_config`).
        Please see :ref:`User Guide <metadata_routing>` on how the routing
        mechanism works.

        The options for each parameter are:

        - ``True``: metadata is requested, and passed to ``fit`` if provided. The request is ignored if metadata is not provided.

        - ``False``: metadata is not requested and the meta-estimator will not pass it to ``fit``.

        - ``None``: metadata is not requested, and the meta-estimator will raise an error if the user provides it.

        - ``str``: metadata should be passed to the meta-estimator with this given alias instead of the original name.

        The default (``sklearn.utils.metadata_routing.UNCHANGED``) retains the
        existing request. This allows you to change the request for some
        parameters and not others.

        .. versionadded:: 1.3

        .. note::
            This method is only relevant if this estimator is used as a
            sub-estimator of a meta-estimator, e.g. used inside a
            :class:`~sklearn.pipeline.Pipeline`. Otherwise it has no effect.

        Parameters
        ----------
        sample_weight : str, True, False, or None,                     default=sklearn.utils.metadata_routing.UNCHANGED
            Metadata routing for ``sample_weight`` parameter in ``fit``.

        Returns
        -------
        self : object
            The updated object.

##### set_params

```python
set_params(self, **params)
```

Set the parameters of this estimator.

        The method works on simple estimators as well as on nested objects
        (such as :class:`~sklearn.pipeline.Pipeline`). The latter have
        parameters of the form ``<component>__<parameter>`` so that it's
        possible to update each component of a nested object.

        Parameters
        ----------
        **params : dict
            Estimator parameters.

        Returns
        -------
        self : estimator instance
            Estimator instance.

##### set_partial_fit_request

```python
set_partial_fit_request(self: sklearn.naive_bayes.MultinomialNB, classes: Union[bool, NoneType, str] = '$UNCHANGED$', sample_weight: Union[bool, NoneType, str] = '$UNCHANGED$')
```

Request metadata passed to the ``partial_fit`` method.

        Note that this method is only relevant if
        ``enable_metadata_routing=True`` (see :func:`sklearn.set_config`).
        Please see :ref:`User Guide <metadata_routing>` on how the routing
        mechanism works.

        The options for each parameter are:

        - ``True``: metadata is requested, and passed to ``partial_fit`` if provided. The request is ignored if metadata is not provided.

        - ``False``: metadata is not requested and the meta-estimator will not pass it to ``partial_fit``.

        - ``None``: metadata is not requested, and the meta-estimator will raise an error if the user provides it.

        - ``str``: metadata should be passed to the meta-estimator with this given alias instead of the original name.

        The default (``sklearn.utils.metadata_routing.UNCHANGED``) retains the
        existing request. This allows you to change the request for some
        parameters and not others.

        .. versionadded:: 1.3

        .. note::
            This method is only relevant if this estimator is used as a
            sub-estimator of a meta-estimator, e.g. used inside a
            :class:`~sklearn.pipeline.Pipeline`. Otherwise it has no effect.

        Parameters
        ----------
        classes : str, True, False, or None,                     default=sklearn.utils.metadata_routing.UNCHANGED
            Metadata routing for ``classes`` parameter in ``partial_fit``.

        sample_weight : str, True, False, or None,                     default=sklearn.utils.metadata_routing.UNCHANGED
            Metadata routing for ``sample_weight`` parameter in ``partial_fit``.

        Returns
        -------
        self : object
            The updated object.

##### set_score_request

```python
set_score_request(self: sklearn.naive_bayes.MultinomialNB, sample_weight: Union[bool, NoneType, str] = '$UNCHANGED$')
```

Request metadata passed to the ``score`` method.

        Note that this method is only relevant if
        ``enable_metadata_routing=True`` (see :func:`sklearn.set_config`).
        Please see :ref:`User Guide <metadata_routing>` on how the routing
        mechanism works.

        The options for each parameter are:

        - ``True``: metadata is requested, and passed to ``score`` if provided. The request is ignored if metadata is not provided.

        - ``False``: metadata is not requested and the meta-estimator will not pass it to ``score``.

        - ``None``: metadata is not requested, and the meta-estimator will raise an error if the user provides it.

        - ``str``: metadata should be passed to the meta-estimator with this given alias instead of the original name.

        The default (``sklearn.utils.metadata_routing.UNCHANGED``) retains the
        existing request. This allows you to change the request for some
        parameters and not others.

        .. versionadded:: 1.3

        .. note::
            This method is only relevant if this estimator is used as a
            sub-estimator of a meta-estimator, e.g. used inside a
            :class:`~sklearn.pipeline.Pipeline`. Otherwise it has no effect.

        Parameters
        ----------
        sample_weight : str, True, False, or None,                     default=sklearn.utils.metadata_routing.UNCHANGED
            Metadata routing for ``sample_weight`` parameter in ``score``.

        Returns
        -------
        self : object
            The updated object.

### TfidfVectorizer

Convert a collection of raw documents to a matrix of TF-IDF features.

    Equivalent to :class:`CountVectorizer` followed by
    :class:`TfidfTransformer`.

    For an example of usage, see
    :ref:`sphx_glr_auto_examples_text_plot_document_classification_20newsgroups.py`.

    For an efficiency comparison of the different feature extractors, see
    :ref:`sphx_glr_auto_examples_text_plot_hashing_vs_dict_vectorizer.py`.

    For an example of document clustering and comparison with
    :class:`~sklearn.feature_extraction.text.HashingVectorizer`, see
    :ref:`sphx_glr_auto_examples_text_plot_document_clustering.py`.

    Read more in the :ref:`User Guide <text_feature_extraction>`.

    Parameters
    ----------
    input : {'filename', 'file', 'content'}, default='content'
        - If `'filename'`, the sequence passed as an argument to fit is
          expected to be a list of filenames that need reading to fetch
          the raw content to analyze.

        - If `'file'`, the sequence items must have a 'read' method (file-like
          object) that is called to fetch the bytes in memory.

        - If `'content'`, the input is expected to be a sequence of items that
          can be of type string or byte.

    encoding : str, default='utf-8'
        If bytes or files are given to analyze, this encoding is used to
        decode.

    decode_error : {'strict', 'ignore', 'replace'}, default='strict'
        Instruction on what to do if a byte sequence is given to analyze that
        contains characters not of the given `encoding`. By default, it is
        'strict', meaning that a UnicodeDecodeError will be raised. Other
        values are 'ignore' and 'replace'.

    strip_accents : {'ascii', 'unicode'} or callable, default=None
        Remove accents and perform other character normalization
        during the preprocessing step.
        'ascii' is a fast method that only works on characters that have
        a direct ASCII mapping.
        'unicode' is a slightly slower method that works on any characters.
        None (default) means no character normalization is performed.

        Both 'ascii' and 'unicode' use NFKD normalization from
        :func:`unicodedata.normalize`.

    lowercase : bool, default=True
        Convert all characters to lowercase before tokenizing.

    preprocessor : callable, default=None
        Override the preprocessing (string transformation) stage while
        preserving the tokenizing and n-grams generation steps.
        Only applies if ``analyzer`` is not callable.

    tokenizer : callable, default=None
        Override the string tokenization step while preserving the
        preprocessing and n-grams generation steps.
        Only applies if ``analyzer == 'word'``.

    analyzer : {'word', 'char', 'char_wb'} or callable, default='word'
        Whether the feature should be made of word or character n-grams.
        Option 'char_wb' creates character n-grams only from text inside
        word boundaries; n-grams at the edges of words are padded with space.

        If a callable is passed it is used to extract the sequence of features
        out of the raw, unprocessed input.

        .. versionchanged:: 0.21
            Since v0.21, if ``input`` is ``'filename'`` or ``'file'``, the data
            is first read from the file and then passed to the given callable
            analyzer.

    stop_words : {'english'}, list, default=None
        If a string, it is passed to _check_stop_list and the appropriate stop
        list is returned. 'english' is currently the only supported string
        value.
        There are several known issues with 'english' and you should
        consider an alternative (see :ref:`stop_words`).

        If a list, that list is assumed to contain stop words, all of which
        will be removed from the resulting tokens.
        Only applies if ``analyzer == 'word'``.

        If None, no stop words will be used. In this case, setting `max_df`
        to a higher value, such as in the range (0.7, 1.0), can automatically detect
        and filter stop words based on intra corpus document frequency of terms.

    token_pattern : str, default=r"(?u)\\b\\w\\w+\\b"
        Regular expression denoting what constitutes a "token", only used
        if ``analyzer == 'word'``. The default regexp selects tokens of 2
        or more alphanumeric characters (punctuation is completely ignored
        and always treated as a token separator).

        If there is a capturing group in token_pattern then the
        captured group content, not the entire match, becomes the token.
        At most one capturing group is permitted.

    ngram_range : tuple (min_n, max_n), default=(1, 1)
        The lower and upper boundary of the range of n-values for different
        n-grams to be extracted. All values of n such that min_n <= n <= max_n
        will be used. For example an ``ngram_range`` of ``(1, 1)`` means only
        unigrams, ``(1, 2)`` means unigrams and bigrams, and ``(2, 2)`` means
        only bigrams.
        Only applies if ``analyzer`` is not callable.

    max_df : float or int, default=1.0
        When building the vocabulary ignore terms that have a document
        frequency strictly higher than the given threshold (corpus-specific
        stop words).
        If float in range [0.0, 1.0], the parameter represents a proportion of
        documents, integer absolute counts.
        This parameter is ignored if vocabulary is not None.

    min_df : float or int, default=1
        When building the vocabulary ignore terms that have a document
        frequency strictly lower than the given threshold. This value is also
        called cut-off in the literature.
        If float in range of [0.0, 1.0], the parameter represents a proportion
        of documents, integer absolute counts.
        This parameter is ignored if vocabulary is not None.

    max_features : int, default=None
        If not None, build a vocabulary that only consider the top
        `max_features` ordered by term frequency across the corpus.
        Otherwise, all features are used.

        This parameter is ignored if vocabulary is not None.

    vocabulary : Mapping or iterable, default=None
        Either a Mapping (e.g., a dict) where keys are terms and values are
        indices in the feature matrix, or an iterable over terms. If not
        given, a vocabulary is determined from the input documents.

    binary : bool, default=False
        If True, all non-zero term counts are set to 1. This does not mean
        outputs will have only 0/1 values, only that the tf term in tf-idf
        is binary. (Set `binary` to True, `use_idf` to False and
        `norm` to None to get 0/1 outputs).

    dtype : dtype, default=float64
        Type of the matrix returned by fit_transform() or transform().

    norm : {'l1', 'l2'} or None, default='l2'
        Each output row will have unit norm, either:

        - 'l2': Sum of squares of vector elements is 1. The cosine
          similarity between two vectors is their dot product when l2 norm has
          been applied.
        - 'l1': Sum of absolute values of vector elements is 1.
          See :func:`~sklearn.preprocessing.normalize`.
        - None: No normalization.

    use_idf : bool, default=True
        Enable inverse-document-frequency reweighting. If False, idf(t) = 1.

    smooth_idf : bool, default=True
        Smooth idf weights by adding one to document frequencies, as if an
        extra document was seen containing every term in the collection
        exactly once. Prevents zero divisions.

    sublinear_tf : bool, default=False
        Apply sublinear tf scaling, i.e. replace tf with 1 + log(tf).

    Attributes
    ----------
    vocabulary_ : dict
        A mapping of terms to feature indices.

    fixed_vocabulary_ : bool
        True if a fixed vocabulary of term to indices mapping
        is provided by the user.

    idf_ : array of shape (n_features,)
        The inverse document frequency (IDF) vector; only defined
        if ``use_idf`` is True.

    See Also
    --------
    CountVectorizer : Transforms text into a sparse matrix of n-gram counts.

    TfidfTransformer : Performs the TF-IDF transformation from a provided
        matrix of counts.

    Examples
    --------
    >>> from sklearn.feature_extraction.text import TfidfVectorizer
    >>> corpus = [
    ...     'This is the first document.',
    ...     'This document is the second document.',
    ...     'And this is the third one.',
    ...     'Is this the first document?',
    ... ]
    >>> vectorizer = TfidfVectorizer()
    >>> X = vectorizer.fit_transform(corpus)
    >>> vectorizer.get_feature_names_out()
    array(['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third',
           'this'], ...)
    >>> print(X.shape)
    (4, 9)

#### Methods

##### __init__

```python
__init__(self, input='content', encoding='utf-8', decode_error='strict', strip_accents=None, lowercase=True, preprocessor=None, tokenizer=None, analyzer='word', stop_words=None, token_pattern='(?u)\\b\\w\\w+\\b', ngram_range=(1, 1), max_df=1.0, min_df=1, max_features=None, vocabulary=None, binary=False, dtype=<class 'numpy.float64'>, norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=False)
```

##### build_analyzer

```python
build_analyzer(self)
```

Return a callable to process input data.

        The callable handles preprocessing, tokenization, and n-grams generation.

        Returns
        -------
        analyzer: callable
            A function to handle preprocessing, tokenization
            and n-grams generation.

##### build_preprocessor

```python
build_preprocessor(self)
```

Return a function to preprocess the text before tokenization.

        Returns
        -------
        preprocessor: callable
              A function to preprocess the text before tokenization.

##### build_tokenizer

```python
build_tokenizer(self)
```

Return a function that splits a string into a sequence of tokens.

        Returns
        -------
        tokenizer: callable
              A function to split a string into a sequence of tokens.

##### decode

```python
decode(self, doc)
```

Decode the input into a string of unicode symbols.

        The decoding strategy depends on the vectorizer parameters.

        Parameters
        ----------
        doc : bytes or str
            The string to decode.

        Returns
        -------
        doc: str
            A string of unicode symbols.

##### fit

```python
fit(self, raw_documents, y=None)
```

Learn vocabulary and idf from training set.

        Parameters
        ----------
        raw_documents : iterable
            An iterable which generates either str, unicode or file objects.

        y : None
            This parameter is not needed to compute tfidf.

        Returns
        -------
        self : object
            Fitted vectorizer.

##### fit_transform

```python
fit_transform(self, raw_documents, y=None)
```

Learn vocabulary and idf, return document-term matrix.

        This is equivalent to fit followed by transform, but more efficiently
        implemented.

        Parameters
        ----------
        raw_documents : iterable
            An iterable which generates either str, unicode or file objects.

        y : None
            This parameter is ignored.

        Returns
        -------
        X : sparse matrix of (n_samples, n_features)
            Tf-idf-weighted document-term matrix.

##### get_feature_names_out

```python
get_feature_names_out(self, input_features=None)
```

Get output feature names for transformation.

        Parameters
        ----------
        input_features : array-like of str or None, default=None
            Not used, present here for API consistency by convention.

        Returns
        -------
        feature_names_out : ndarray of str objects
            Transformed feature names.

##### get_metadata_routing

```python
get_metadata_routing(self)
```

Get metadata routing of this object.

        Please check :ref:`User Guide <metadata_routing>` on how the routing
        mechanism works.

        Returns
        -------
        routing : MetadataRequest
            A :class:`~sklearn.utils.metadata_routing.MetadataRequest` encapsulating
            routing information.

##### get_params

```python
get_params(self, deep=True)
```

Get parameters for this estimator.

        Parameters
        ----------
        deep : bool, default=True
            If True, will return the parameters for this estimator and
            contained subobjects that are estimators.

        Returns
        -------
        params : dict
            Parameter names mapped to their values.

##### get_stop_words

```python
get_stop_words(self)
```

Build or fetch the effective stop words list.

        Returns
        -------
        stop_words: list or None
                A list of stop words.

##### inverse_transform

```python
inverse_transform(self, X)
```

Return terms per document with nonzero entries in X.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            Document-term matrix.

        Returns
        -------
        X_inv : list of arrays of shape (n_samples,)
            List of arrays of terms.

##### set_params

```python
set_params(self, **params)
```

Set the parameters of this estimator.

        The method works on simple estimators as well as on nested objects
        (such as :class:`~sklearn.pipeline.Pipeline`). The latter have
        parameters of the form ``<component>__<parameter>`` so that it's
        possible to update each component of a nested object.

        Parameters
        ----------
        **params : dict
            Estimator parameters.

        Returns
        -------
        self : estimator instance
            Estimator instance.

##### transform

```python
transform(self, raw_documents)
```

Transform documents to document-term matrix.

        Uses the vocabulary and document frequencies (df) learned by fit (or
        fit_transform).

        Parameters
        ----------
        raw_documents : iterable
            An iterable which generates either str, unicode or file objects.

        Returns
        -------
        X : sparse matrix of (n_samples, n_features)
            Tf-idf-weighted document-term matrix.

